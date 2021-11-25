import base64
import io
import json
import os
import tarfile
import tempfile
from tarfile import TarFile
from typing import Any, Dict, Iterable, List, Tuple

import apache_beam as beam
from apache_beam.io.filesystems import FileSystems as beam_fs
from apache_beam.options.pipeline_options import PipelineOptions


def expand_pattern(pattern: str) -> Iterable[str]:
    for match_result in beam_fs.match([pattern])[0].metadata_list:
        yield match_result.path


def blob_filepath_to_bytes(filepath: str) -> Iterable[Tuple[str, bytes]]:
    with open(filepath, "rb") as f:
        data = f.read()
        blob_bytes_data = base64.b64encode(data)
        blob_name = filepath.split("/")[1]

        yield (blob_name, blob_bytes_data)


def blob_json_content(blob, member):
    with blob.extractfile(member) as file:
        return json.load(file)


def create_blob(blob_name, metadata, result) -> bytes:
    with tempfile.TemporaryDirectory() as tmp_dir:

        metadata_path = os.path.join(tmp_dir, "metadata.json")
        with open(metadata_path, "w") as mf:
            mf.write(json.dumps(metadata))

        result_path = os.path.join(tmp_dir, "result.json")
        with open(result_path, "w") as rf:
            rf.write(json.dumps(result))

        file_path = os.path.join(tmp_dir, blob_name)
        with tarfile.open(name=file_path, mode="w:gz") as blob:
            blob.add(metadata_path, "metadata.json")
            blob.add(result_path, "result.json")

        with open(file_path, "rb") as bf:
            data = bf.read()
            return base64.b64encode(data)


def fix_blob_data(blob: Tuple[str, bytes]) -> Iterable[Tuple[str, bytes]]:
    (blob_name, blob_bytes_data) = blob

    file_like_object = io.BytesIO(base64.b64decode(blob_bytes_data))
    with tarfile.open(fileobj=file_like_object, mode="r:gz") as blob_file:
        metadata_content = blob_json_content(blob_file, "metadata.json")
        result_content = blob_json_content(blob_file, "result.json")
        metadata_content["check_name"] = blob_name.split("-")[0]

        new_blob_bytes_data = create_blob(blob_name, metadata_content, result_content)

        yield (blob_name, new_blob_bytes_data)


def bytes_to_blob_filepath(blob: Tuple[str, bytes], file_name_prefix: str) -> None:
    (blob_name, blob_bytes_data) = blob
    file_like_object = io.BytesIO(base64.b64decode(blob_bytes_data))

    path = os.path.join(file_name_prefix, blob_name)
    with open(path, "wb") as f:
        f.write(file_like_object.getvalue())


input_patterns = ["blobs/*.tar.gz"]
output_prefix = "clean_blobs_2_bytes/"
options = PipelineOptions(flags=[], type_check_additional="all")

with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | "Create file patterns" >> beam.Create(input_patterns)
        | "Expand file patterns" >> beam.FlatMap(expand_pattern)
        | "Read blob" >> beam.FlatMap(blob_filepath_to_bytes)
        | "Fix check name" >> beam.FlatMap(fix_blob_data)
        | "Write blob" >> beam.Map(bytes_to_blob_filepath, output_prefix)
    )

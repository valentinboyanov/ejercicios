import json
import os
import tarfile
import tempfile
from typing import Any, Dict, Iterable, List

import apache_beam as beam
from apache_beam.io.filesystems import FileSystems as beam_fs
from apache_beam.options.pipeline_options import PipelineOptions


def expand_pattern(pattern: str) -> Iterable[str]:
    for match_result in beam_fs.match([pattern])[0].metadata_list:
        yield match_result.path


def blob_json_content(blob, member):
    with blob.extractfile(member) as file:
        return json.load(file)


def read_blob_files(file_name: str) -> Iterable[Dict[str, Any]]:
    with tarfile.open(name=file_name, mode="r:gz") as blob:
        blob_name = file_name.split("/")[1]
        metadata_content = blob_json_content(blob, "metadata.json")
        result_content = blob_json_content(blob, "result.json")
        yield {
            "blob_name": blob_name,
            "metadata": metadata_content,
            "result": result_content,
        }


def check_name(blob_name):
    return blob_name.split("-")[0]


def fix_check_name(blob_content: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    blob_content["metadata"]["check_name"] = check_name(blob_content["blob_name"])
    yield blob_content


def create_blob(name, metadata, result, dir):
    with tempfile.TemporaryDirectory() as tmp_dir:

        metadata_path = os.path.join(tmp_dir, "metadata.json")
        with open(metadata_path, "w") as f:
            f.write(json.dumps(metadata))

        result_path = os.path.join(tmp_dir, "result.json")
        with open(result_path, "w") as f:
            f.write(json.dumps(result))

        blob_path = os.path.join(dir, name)
        with tarfile.open(name=blob_path, mode="w:gz") as blob:
            blob.add(metadata_path, "metadata.json")
            blob.add(result_path, "result.json")


def write_blob(content: Dict[str, Any], file_name_prefix: str):
    blob_name = content["blob_name"]
    metadata = content["metadata"]
    result = content["result"]
    create_blob(blob_name, metadata, result, file_name_prefix)


input_patterns = ["blobs/*.tar.gz"]
output_prefix = "clean_blobs_2/"
options = PipelineOptions(flags=[], type_check_additional="all")

with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | "Create file patterns" >> beam.Create(input_patterns)
        | "Expand file patterns" >> beam.FlatMap(expand_pattern)
        | "Read blob" >> beam.FlatMap(read_blob_files)
        | "Fix check name" >> beam.FlatMap(fix_check_name)
        | "Write blob" >> beam.Map(write_blob, output_prefix)
    )

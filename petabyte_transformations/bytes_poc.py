import base64
import io
import json
import os
import tarfile
import tempfile
from tarfile import TarFile
from typing import Tuple


def blob_filepath_to_bytes(filepath: str) -> Tuple[str, bytes]:
    with open(filepath, "rb") as f:
        data = f.read()
        blob_bytes_data = base64.b64encode(data)
        blob_name = filepath.split("/")[2]

        return (blob_name, blob_bytes_data)


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


def fix_blob_data(blob: Tuple[str, bytes]) -> Tuple[str, bytes]:
    (blob_name, blob_bytes_data) = blob

    file_like_object = io.BytesIO(base64.b64decode(blob_bytes_data))
    with tarfile.open(fileobj=file_like_object, mode="r:gz") as blob_file:
        metadata_content = blob_json_content(blob_file, "metadata.json")
        result_content = blob_json_content(blob_file, "result.json")
        metadata_content["check_name"] = blob_name.split("-")[0]

        new_blob_bytes_data = create_blob(blob_name, metadata_content, result_content)

        return (blob_name, new_blob_bytes_data)


def bytes_to_blob_filepath(blob: Tuple[str, bytes]) -> None:
    (blob_name, blob_bytes_data) = blob
    file_like_object = io.BytesIO(base64.b64decode(blob_bytes_data))

    path = os.path.join("./", blob_name)
    with open(path, "wb") as f:
        f.write(file_like_object.getvalue())


if __name__ == "__main__":
    file_path = "./blobs/check_404-2021-08-31T12:49:19.003135.tar.gz"

    data_bytes = blob_filepath_to_bytes(file_path)
    print(data_bytes)
    print()

    fixed_data_bytes = fix_blob_data(data_bytes)
    print(fixed_data_bytes)
    print()

    bytes_to_blob_filepath(fixed_data_bytes)

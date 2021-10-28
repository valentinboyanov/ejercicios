import json
import os
import tarfile
import tempfile
from typing import Dict, List

BLOBS_PATH = "./blobs"
CLEAN_BLOBS_PATH = "./clean_blobs_1"


def bad_blobs_list(dir: str) -> List[str]:
    bad_blobs: List[str] = []

    for name in os.listdir(dir):
        blob_path = os.path.join(dir, name)
        with tarfile.open(name=blob_path) as blob:
            metadata = blob_json_content(blob, "metadata.json")
            if metadata["check_name"] != check_name(name):
                bad_blobs.append(name)

    return bad_blobs


def clean_blobs(origin_dir: str, dest_dir: str) -> None:
    for blob_name in os.listdir(origin_dir):
        blob_path = os.path.join(origin_dir, blob_name)
        with tarfile.open(name=blob_path, mode="r:gz") as blob:
            metadata = blob_json_content(blob, "metadata.json")
            result = blob_json_content(blob, "result.json")
            metadata["check_name"] = check_name(blob_name)
            create_blob(name=blob_name, metadata=metadata, result=result, dir=dest_dir)


def create_blob(name: str, metadata: Dict, result: Dict, dir: str) -> None:
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


def check_name(blob_name: str) -> str:
    return blob_name.split("-")[0]


def blob_json_content(blob, member: str) -> Dict:
    with blob.extractfile(member) as file:
        return json.load(file)


if __name__ == "__main__":
    os.makedirs(CLEAN_BLOBS_PATH)

    clean_blobs(BLOBS_PATH, CLEAN_BLOBS_PATH)

    bad_blobs_before_cleaning = bad_blobs_list(BLOBS_PATH)
    print("Bad blobs before cleaning: {0}".format(len(bad_blobs_before_cleaning)))
    for b in bad_blobs_before_cleaning:
        print(b)

    bad_blobs_after_cleaning = bad_blobs_list(CLEAN_BLOBS_PATH)
    print("\n\nBad blobs after cleaning: {0}".format(len(bad_blobs_after_cleaning)))
    for b in bad_blobs_after_cleaning:
        print(b)

import urllib.parse

from mandible.log import init_root_logger, log_errors
from run_cumulus_task import run_cumulus_task


def cnm_to_granules(event: dict, _) -> dict:
    payload = event["input"]
    granule = {
        "granuleId": payload["product"]["name"],
        "files": [
            cnm_file_to_granules_file(file)
            for file in payload["product"]["files"]
        ]
    }
    return {
        "granules": [granule],
        "cnm": payload
    }


def cnm_file_to_granules_file(file: dict) -> dict:
    uri = file["uri"]
    parsed_uri = urllib.parse.urlparse(uri)

    if not parsed_uri.path[1:]:
        raise RuntimeError(f"Invalid URI in CNM: '{uri}'")

    key_prefix, key_name = parsed_uri.path.rsplit("/", 1)

    return {
        "source_bucket": parsed_uri.netloc,
        "path": key_prefix[1:],
        "name": file["name"],
        "size": file["size"],
        "type": file["type"],
        "checksum": file["checksum"],
        "checksumType": file["checksumType"]
    }


def lambda_handler(event: dict, context: dict):
    init_root_logger()
    with log_errors():
        return run_cumulus_task(cnm_to_granules, event, context)

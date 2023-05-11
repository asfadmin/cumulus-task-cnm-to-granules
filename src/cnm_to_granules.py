from urllib.parse import urlparse

from mandible.log import init_root_logger, log_errors
from run_cumulus_task import run_cumulus_task


def cnm_to_granules(event: dict, _) -> dict:
    payload = event["input"]
    granule = {
        "granuleId": payload["product"]["name"],
        "files": [
            {
                "source_bucket": urlparse(file["uri"]).netloc,
                "path": urlparse(file["uri"]).path[1:].rsplit("/", 1)[0],
                "name": file["name"],
                "type": file["type"],
                "checksum": file["checksum"],
                "checksumType": file["checksumType"]
            }
            for file in payload["product"]["files"]
        ]
    }
    return {
        "granules": [granule],
        "cnm": payload
    }


def lambda_handler(event: dict, context: dict):
    init_root_logger()
    with log_errors():
        return run_cumulus_task(cnm_to_granules, event, context)

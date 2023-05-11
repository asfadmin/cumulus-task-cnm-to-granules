import logging
import os
from contextlib import contextmanager
from typing import Type
from urllib.parse import urlparse

from run_cumulus_task import run_cumulus_task


# Copied from https://github.com/asfadmin/mandible
def init_root_logger():
    """Set up log levels for lambda using the environment variable"""
    level = os.getenv("LOG_LEVEL", logging.INFO)

    logging.getLogger().setLevel(level)
    logging.getLogger("boto3").setLevel(logging.INFO)
    logging.getLogger("botocore").setLevel(logging.INFO)


@contextmanager
def log_errors(*exceptions: Type[BaseException]):
    exceptions = exceptions or (BaseException,)
    try:
        yield
    except exceptions as e:
        logging.exception("%s: %s", e.__class__.__name__, e)
        raise


def cnm_to_cma(event: dict, _) -> dict:
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
        return run_cumulus_task(cnm_to_cma, event, context)

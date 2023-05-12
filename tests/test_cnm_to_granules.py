from cnm_to_granules import cnm_to_granules, lambda_handler

cnm = {
    "identifier": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021",
    "collection": "FOE",
    "version": "1.5",
    "submissionTime": "2023-03-28T15:45:46.985706Z",
    "product": {
        "name": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021",
        "files": [
            {
                "name": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021.xml",
                "type": "data",
                "uri": (
                    "s3://mrp-n-cumulus-dev-nisar-landing/"
                    "testing/FOE/1/NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021.xml"
                ),
                "size": 120250,
                "checksum": "6cace6cc9877aa8ecfb5786cc764d267",
                "checksumType": "md5",
            }
        ],
        "dataVersion": "1.0",
    },
    "provider": "ASFDEV",
}


def test_lambda_handler():
    event = {
        "cma": {
            "task_config": {
                "cumulus_message": {
                    "outputs": [
                        {
                            "source": "{$.granules}",
                            "destination": "{$.payload.granules}",
                        },
                        {"source": "{$.cnm}", "destination": "{$.meta.cnm}"},
                    ]
                }
            },
            "event": {
                "cumulus_meta": {},
                "exception": None,
                "meta": {
                    "buckets": {},
                    "cmr": {},
                    "collection": {},
                    "distribution_endpoint": "https://uqpgf5nty5.execute-api.us-west-2.amazonaws.com/dev/",
                    "launchpad": {},
                    "provider": {},
                    "stack": "mrp-cumulus-dev",
                    "template": "s3://mrp-cumulus-dev-internal/mrp-cumulus-dev/workflow_template.json",
                    "workflow_name": "OPERAWorkflow",
                    "workflow_tasks": {},
                    "retries": 3,
                    "provider_path": "/",
                    "visibilityTimeout": 300,
                    "eventSource": {},
                },
                "payload": cnm,
            },
        }
    }
    lambda_handler(event, None)


def test_cnm_to_granules():
    event = {"input": cnm}

    assert cnm_to_granules(event, None) == {
        "cnm": {
            "identifier": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021",
            "collection": "FOE",
            "version": "1.5",
            "submissionTime": "2023-03-28T15:45:46.985706Z",
            "product": {
                "name": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021",
                "files": [
                    {
                        "name": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021.xml",
                        "type": "data",
                        "uri": (
                            "s3://mrp-n-cumulus-dev-nisar-landing/testing/"
                            "FOE/1/NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021.xml"
                        ),
                        "size": 120250,
                        "checksum": "6cace6cc9877aa8ecfb5786cc764d267",
                        "checksumType": "md5",
                    }
                ],
                "dataVersion": "1.0",
            },
            "provider": "ASFDEV",
        },
        "granules": [
            {
                "files": [
                    {
                        "name": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021.xml",
                        "path": "testing/FOE/1",
                        "source_bucket": "mrp-n-cumulus-dev-nisar-landing",
                        "checksum": "6cace6cc9877aa8ecfb5786cc764d267",
                        "checksumType": "md5",
                        "type": "data",
                    }
                ],
                "granuleId": "NISAR_ANC_L_PR_FOE_20220815T184157_20230701T000800_20230701T001021",
            }
        ],
    }

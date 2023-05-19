# CNM to Granules - Cumulus Task
A cumulus task for converting CNM messages into the CMA input format expected
by SyncGranule.

## Deployment Example
There is an example of how to add the lambda to your cumulus deployment in the
[example](example/) directory. The example assumes you have deployed Cumulus
with [CIRRUS](https://github.com/asfadmin/CIRRUS-core/).

To deploy the example, set your aws profile and region to the correct values
and enter the appropriate values for `DEPLOY_NAME` and `prefix` when prompted:

```
$ cd example
$ terraform init
$ AWS_PROFILE=example-aws-profile AWS_REGION=us-west-2 terraform apply
var.DEPLOY_NAME
  Enter a value: example

var.prefix
  Enter a value: example-cumulus-dev
```

## Usage Example
To use the task, add it as the first step in your ingest workflow followed by
SyncGranule.

```json
{
  "Comment": "Example CNM Ingest Workflow",
  "StartAt": "CnmToGranules",
  "States": {
    "CnmToGranules": {
      "Type": "Task",
      "Resource": "${CnmToGranulesArn}",
      "Parameters": {
        "cma": {
          "event.$": "$",
          "task_config": {
            "cumulus_message": {
              "outputs": [
                {
                  "source": "{$.granules}",
                  "destination": "{$.payload.granules}"
                },
                {
                  "source": "{$.cnm}",
                  "destination": "{$.meta.cnm}"
                }
              ]
            }
          }
        }
      },
      "Next": "SyncGranule"
    },
    "SyncGranule": {
      "Type": "Task",
      "Resource": "${SyncGranuleArn}",
      "Parameters": {
        "cma": {
          "event.$": "$",
          "task_config": {
            "ACL": "disabled",
            "buckets": "{$.meta.buckets}",
            "stack": "{$.meta.stack}",
            "downloadBucket": "{$.meta.buckets.products.name}",
            "duplicateHandling": "{$.meta.collection.duplicateHandling}",
            "provider": "{$.meta.provider}",
            "collection": "{$.meta.collection}",
            "workflowStartTime": "{$.cumulus_meta.workflow_start_time}",
            "syncChecksumFiles": true
          },
          "cumulus_message": {
            "input": "{$.payload}",
            "outputs": [
              {
                "source": "{$.granules}",
                "destination": "{$.meta.input_granules}"
              },
              {
                "source": "{$}",
                "destination": "{$.payload}"
              },
              {
                "source": "{$.process}",
                "destination": "{$.meta.process}"
              }
            ]
          }
        }
      },
      "End": true
    },
    "WorkflowFailed": {
      "Type": "Fail",
      "Cause": "Workflow failed"
    }
  }
}

```

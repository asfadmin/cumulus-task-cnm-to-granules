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

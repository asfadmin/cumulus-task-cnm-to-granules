resource "aws_lambda_function" "cnm_to_cma_task" {
  function_name    = "${var.prefix}-CnmToCma"
  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")
  handler          = "cnm_to_cma.lambda_handler"
  role             = var.lambda_processing_role_arn
  runtime          = "python3.9"
  timeout          = var.cnm_to_cma_task_timeout
  memory_size      = var.cnm_to_cma_task_memory_size

  environment {
    variables = {
      stackName                   = var.prefix
      system_bucket               = var.system_bucket
      CUMULUS_MESSAGE_ADAPTER_DIR = "/opt/"
    }
  }

  dynamic "vpc_config" {
    for_each = length(var.lambda_subnet_ids) == 0 ? [] : [1]
    content {
      subnet_ids = var.lambda_subnet_ids
      security_group_ids = [
        aws_security_group.no_ingress_all_egress[0].id
      ]
    }
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "cnm_to_cma_task" {
  name              = "/aws/lambda/${aws_lambda_function.cnm_to_cma_task.function_name}"
  retention_in_days = 30
  tags              = var.tags
}

output "cnm_to_granules_task" {
  value = {
    task_arn           = aws_lambda_function.cnm_to_granules_task.arn
    last_modified_date = aws_lambda_function.cnm_to_granules_task.last_modified
  }
}

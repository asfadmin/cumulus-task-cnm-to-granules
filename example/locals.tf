locals {
  lambda_subnet_ids         = data.terraform_remote_state.cumulus.outputs.subnet_ids
  lambda_security_group_ids = [data.terraform_remote_state.cumulus.outputs.no_ingress_all_egress.id]

  cumulus_remote_state_config = {
    bucket = "${var.prefix}-tf-state-${substr(data.aws_caller_identity.current.account_id, -4, 4)}"
    key    = "cumulus/terraform.tfstate"
    region = data.aws_region.current.name
  }

  log_level = "INFO"
}

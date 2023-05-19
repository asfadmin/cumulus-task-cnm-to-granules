terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0,!= 3.14.0"
    }
  }
  required_version = ">= 0.13"
}


module "cnm_to_granules_task" {
  source = "../build/terraform"

  prefix                     = var.prefix
  lambda_subnet_ids          = local.lambda_subnet_ids
  lambda_security_group_ids  = local.lambda_security_group_ids
  lambda_processing_role_arn = data.terraform_remote_state.cumulus.outputs.lambda_processing_role_arn
  tags = {
    Deployment = "cnm_to_granules_task example"
  }
}

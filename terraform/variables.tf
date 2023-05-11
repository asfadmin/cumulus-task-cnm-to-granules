variable "lambda_processing_role_arn" {
  type = string
}

variable "lambda_subnet_ids" {
  type    = list(string)
  default = []
}

variable "prefix" {
  type = string
}

variable "system_bucket" {
  type = string
}

variable "tags" {
  description = "Tags to be applied to managed resources"
  type        = map(string)
  default     = {}
}

variable "cnm_to_cma_task_memory_size" {
  description = "Memory size for ingest task lambda"
  type        = number
  default     = 1024
}

variable "cnm_to_cma_task_timeout" {
  description = "Timeout for ingest task lambda"
  type        = number
  default     = 300
}

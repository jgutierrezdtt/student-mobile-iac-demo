variable "aws_region" {
  description = "Region de AWS donde se despliegan los recursos"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Nombre del entorno (prod, staging, dev)"
  type        = string
}

variable "app_bucket_name" {
  description = "Nombre del bucket S3 de la aplicacion"
  type        = string
}

# ---------------------------------------------------------------------------
# Secretos — todos vienen de AWS SSM Parameter Store, no tienen defaults
# ---------------------------------------------------------------------------

data "aws_ssm_parameter" "api_key" {
  name            = "/${var.environment}/app/api_key"
  with_decryption = true
}

data "aws_ssm_parameter" "jwt_secret" {
  name            = "/${var.environment}/app/jwt_secret"
  with_decryption = true
}

# ---------------------------------------------------------------------------
# Outputs — los valores sensibles se marcan para que no aparezcan en logs
# ---------------------------------------------------------------------------

# TODO (step 05): los outputs exponen valores secretos en los logs de Terraform.
# Lee el paso 05 en .tutorial/steps/05-secretos-en-iac.md
# para aprender como ocultar estos valores en los outputs.
output "api_key" {
  description = "API key de la aplicacion"
  value       = data.aws_ssm_parameter.api_key.value
}

output "jwt_secret" {
  description = "Secret para firmar JWT"
  value       = data.aws_ssm_parameter.jwt_secret.value
}

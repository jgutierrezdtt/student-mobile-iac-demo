locals {
  app_bucket_arn = aws_s3_bucket.app_bucket.arn
  ssm_path_arn   = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.environment}/app/*"
}

data "aws_caller_identity" "current" {}

# ---------------------------------------------------------------------------
# IAM Role para la funcion Lambda de la aplicacion
# ---------------------------------------------------------------------------

resource "aws_iam_role" "lambda_exec" {
  name = "${var.environment}-lambda-app-exec"

  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Environment = var.environment
  }
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    sid    = "LambdaAssumeRole"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# Politica con permisos para la funcion Lambda
data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      local.app_bucket_arn,
      "${local.app_bucket_arn}/*"
    ]
  }

  statement {
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters"
    ]
    resources = [local.ssm_path_arn]
  }

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.environment}-app:*"
    ]
  }
}

resource "aws_iam_policy" "lambda_policy" {
  name   = "${var.environment}-lambda-app-policy"
  policy = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

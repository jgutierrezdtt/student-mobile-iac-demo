terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "myapp-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
}

# ---------------------------------------------------------------------------
# S3 bucket — almacenamiento de artefactos de aplicacion
# ---------------------------------------------------------------------------
resource "aws_s3_bucket" "app_bucket" {
  bucket = var.app_bucket_name

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# TODO (step 04): el bucket no tiene bloqueo de acceso publico.
# Lee el paso 04 en .tutorial/steps/04-iac-misconfigurations.md
# para anadir el recurso de bloqueo y hacer la base de datos no publica.

resource "aws_s3_bucket_versioning" "app_bucket" {
  bucket = aws_s3_bucket.app_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_bucket" {
  bucket = aws_s3_bucket.app_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

# ---------------------------------------------------------------------------
# VPC y Security Groups
# ---------------------------------------------------------------------------
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_security_group" "app_sg" {
  name        = "${var.environment}-app-sg"
  description = "Security group para la aplicacion"
  vpc_id      = aws_vpc.main.id

  # SEGURO: SSH solo desde la VPN corporativa, no desde internet
  ingress {
    description = "SSH desde VPN corporativa"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Todo el trafico saliente"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-app-sg"
    Environment = var.environment
  }
}

# ---------------------------------------------------------------------------
# RDS — base de datos de la aplicacion
# ---------------------------------------------------------------------------
resource "aws_db_instance" "main" {
  identifier        = "${var.environment}-app-db"
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = "appdb"
  username = "appuser"
  password = data.aws_ssm_parameter.db_password.value

  # TODO (step 04): la base de datos es accesible desde internet.
  # Cambia a publicly_accessible = false
  publicly_accessible = true
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  storage_encrypted = true

  backup_retention_period = 7
  deletion_protection     = true

  tags = {
    Environment = var.environment
  }
}

data "aws_ssm_parameter" "db_password" {
  name            = "/${var.environment}/db/password"
  with_decryption = true
}

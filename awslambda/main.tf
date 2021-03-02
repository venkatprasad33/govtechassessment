
////////////////////////////////
// AWS Lambda Setup
////////////////////////////////

// provider
provider "aws" {
    profile = "default"
    region = "us-west-2"
}

// variables
variable "function_name" {
  type  = string
}

variable "role_name" {
  type = string
}

// to adopt existing default vpc subnets in terraform.
resource "aws_default_vpc" "default" {}

resource "aws_default_subnet" "default_az1" {
  availability_zone = "us-west-2a"
}

resource "aws_default_subnet" "default_az2" {
  availability_zone = "us-west-2b"
}

resource "aws_default_security_group" "default" {}

resource "aws_iam_role" "govtech" {
    name = var.role_name
    assume_role_policy =<<EOF
{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
}
EOF
    tags = {
     "Terraform" = "true"
   }
}

data "aws_iam_policy" "govtech" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy_attachment" "govtech" {
  role = aws_iam_role.govtech.name
  policy_arn = data.aws_iam_policy.govtech.arn
}

resource "aws_lambda_function" "govtech" {
   function_name = var.function_name
   role = aws_iam_role.govtech.arn
   handler = "index.handler"
   runtime = "python3.8"
   filename = "lambda_function.zip"
   source_code_hash = data.archive_file.govtech.output_base64sha256
   timeout = 30
   memory_size = 128

   vpc_config {
     subnet_ids = [
         aws_default_subnet.default_az1.id,
         aws_default_subnet.default_az2.id
     ]
     security_group_ids = [
         aws_default_security_group.default.id
     ]
   }

   tags = {
     "Terraform" = "true"
   }
}

data "archive_file" "govtech" {
   type = "zip"
   source_file = "index.py"
   output_path = "lambda_function.zip"
}
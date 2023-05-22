terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_instance" "app_server" {
  ami           = "ami-08333bccc35d71140"
  instance_type = var.instance_type
  key_name      = "ec2-master"

  user_data = file("${path.module}/airflow_startup.sh")

  tags = {
    Name = var.instance_name
  }
}

resource "aws_security_group" "dumb_sg" {
  name        = "dumb_sg"
  description = "allow all tcp traffic rn - dont do this in prod"


  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_everything"
  }
}

resource "aws_network_interface_sg_attachment" "sg_attachment" {
  security_group_id    = aws_security_group.dumb_sg.id
  network_interface_id = aws_instance.app_server.primary_network_interface_id
}

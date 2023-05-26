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


resource "aws_security_group" "dumb_db_sg" {
  name        = "dumb_db_sg"
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


resource "aws_db_instance" "default" {
  allocated_storage    = 10
  db_name              = "reddit_cat_pics"
  engine               = "mysql"
  engine_version       = "8.0.32"
  instance_class       = "db.t3.micro"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
  publicly_accessible  = true
  vpc_security_group_ids = [aws_security_group.dumb_db_sg.id]

}



resource "aws_s3_bucket" "cat_pics" {
  bucket = "cat-pics"

  tags = {
    Name        = "CATS CATS CATS"
  }
}
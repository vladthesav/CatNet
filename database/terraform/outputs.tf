output "cat_pic_db_endpoint" {
  description = "endpoint of reddit catpic db"
  value       = aws_db_instance.default.address
}
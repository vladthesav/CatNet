variable "instance_name" {
  description = "Value of the Name tag for the EC2 instance"
  type        = string
  default     = "airflow_server"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.medium"

}
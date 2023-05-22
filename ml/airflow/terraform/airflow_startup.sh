#!/bin/bash
yum update -y
yum install python3-pip -y
yum install docker -y 
service docker restart

pip -V > pip_v
pip install apache-airflow > wtf
airflow > plz_work 


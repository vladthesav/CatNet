#!/bin/bash
yum update -y
yum install python3-pip -y

#install docker
yum install docker -y 
service docker restart

#install docker compose
#curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
#sudo chmod +x /usr/local/bin/docker-compose
#docker-compose version



#get apache airflow container and run it
#ty https://stackoverflow.com/questions/63658263/how-do-i-deploy-my-airflow-scheduler-to-aws-ec2
docker pull puckel/docker-airflow
#docker run -d -p 8080:8080 puckel/docker-airflow webserver
docker run -d -p 8080:8080 -v dags:/usr/local/airflow/dags  puckel/docker-airflow webserver

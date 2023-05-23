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

#get code from github
yum install git -y
git clone --branch lambda-data-ingestion https://github.com/vladthesav/CatNet.git
#get apache airflow container and run it
docker pull apache/airflow
docker run -p 8080:8080 -v $(pwd)/dags:/opt/airflow/dags apache/airflow standalone > docker_logs


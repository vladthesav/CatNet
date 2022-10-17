FROM bitnami/pytorch:latest

#RUN apt-get update -y && \
#    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 3500

#set this env variable so programs know it's running in a container
ENV container=True 

CMD ["python3","server.py"]
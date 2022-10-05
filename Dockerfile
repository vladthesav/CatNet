FROM jazzdd/alpine-flask

RUN pip install requests

WORKDIR /app

COPY . /app

EXPOSE 3500  

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
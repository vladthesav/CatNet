FROM jazzdd/alpine-flask

WORKDIR /app

COPY . /app

EXPOSE 80  

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
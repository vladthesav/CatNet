FROM jazzdd/alpine-flask

WORKDIR /app

COPY . /app

EXPOSE 3500  

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
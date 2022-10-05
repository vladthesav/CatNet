from flask import Flask
from requests import get

#get container IP
ip = get('https://api.ipify.org').text

app = Flask(__name__)

@app.route("/")
def test(): return "hello from {}\n".format(ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 3500)
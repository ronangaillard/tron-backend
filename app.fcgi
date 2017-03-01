#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from mainapp import app
from flask_cors import CORS, cross_origin

if __name__ == '__main__':
    CORS(app, supports_credentials = True)
    WSGIServer(app, bindAddress="/tmp/tron-back-end-fcgi.sock").run()

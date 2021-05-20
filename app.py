import config
from flask import Flask, Response, request, jsonify
import json, re, requests
import rq
from redis import Redis

app = Flask(__name__)

queue = rq.Queue(name='default', connection=Redis(host='fr-redis'))

@app.route('/')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run()


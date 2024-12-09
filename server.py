import threading

import requests
from flask import Flask, request
from runme import run

app = Flask(__name__)

@app.post('/simulate')
def trigger_simulation():
    threading.Thread(target=simulate, args=[request.get_json()]).start()
    return "Simulation started"


def simulate(config):
    requests.post(config['callback'], json=run(config))

if __name__ == '__main__':
    app.run()

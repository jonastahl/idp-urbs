from flask import Flask, request
from runme import run

app = Flask(__name__)

@app.post('/simulate')
def simulate():
    config = request.get_json()
    return run(config)

if __name__ == '__main__':
    app.run()

from flask import Flask, request
from runme import run

app = Flask(__name__)

buffer = dict()

@app.post('/simulate')
def simulate():
    global buffer
    if request.data in buffer:
        print("Found in buffer")
        return buffer[request.data]
    print("Not found in buffer -> simulating")
    config = request.get_json()
    result = run(config)
    buffer[request.data] = result
    return result

if __name__ == '__main__':
    app.run()

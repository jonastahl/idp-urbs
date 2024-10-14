from flask import Flask
from runme import run

app = Flask(__name__)

@app.get('/simulate')
def simulate():
    run()
    return "success!"

if __name__ == '__main__':
    app.run()

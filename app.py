import time
from flask import Flask


app = Flask(__name__)

@app.route('/carrito', methods=['GET'])
def carrito():
    return f'Hello carrito! {200} OK'


@app.route('/comprar', methods=['POST'])
def comprar():
    time.sleep(0.2)
    return f'Hello comprar! {200} OK'


if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")
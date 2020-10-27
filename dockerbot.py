from flask import Flask
from flask import Api


app = Flask(__name__)
api = Api(app)

@app.route('/')
def getStatement():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6700)

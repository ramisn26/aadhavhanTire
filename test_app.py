from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return 'Hello! The application is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
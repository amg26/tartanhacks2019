from flask import Flask
app = Flask(__name__)

# What a time

@app.route("/")
def hello():
    return "Hello World!"
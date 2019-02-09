<<<<<<< HEAD
from flask import Flask
app = Flask(__name__)

# What a time
# Another comment

@app.route("/")
def hello():
=======
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
>>>>>>> a24f30285c344de59f90769f4271bb1b467ec520
    return "Hello World!"
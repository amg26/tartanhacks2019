from flask import Flask, request, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
def index() :
	return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
	return 'nice ' + request.form['join_code']
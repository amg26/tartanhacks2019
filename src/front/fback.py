from flask import Flask, request, render_template, session
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'slqclkekql-12cumiojkwfa-fo2i4c2ic4flajkfa'

@app.route('/', methods=['GET'])
def index() :
	if session.get('join_code') is not None:
		return 'you are already a part of: ' + session['join_code']
	return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
	# need to check if join code is valid and add user to that event

	session['join_code'] = request.form['join_code']
	return 'nice ' + request.form['join_code']

@app.route('/userprofile', methods=['GET'])
def userprofile() :
	return render_template('testing.html')

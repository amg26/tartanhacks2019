from flask import Flask, request, render_template, session
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import ArgumentValidationError, validate_arguments

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'slqclkekql-12cumiojkwfa-fo2i4c2ic4flajkfa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "user_uploads"


'''Add database'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	username = db.Column(db.String(80), primary_key=True)
	firstName = db.Column(db.String(80), unique = False, nullable = False)
	age = db.Column(db.Integer, unique = False, nullable = True)
	profilePic = db.Column(db.LargeBinary, unique = True, nullable = True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	passions = db.Column(db.String(80), unique = False, nullable = True)
	hometown = db.Column(db.String(80), unique = False, nullable = False)
	bio = db.Column(db.String(300), unique = False, nullable = True)
	
	

	def __repr__(self):
		return '<User %r>' % self.usernamee
		
		
class UserAPI(MethodView):

	def get(self, user_id):
		if user_id is None:
			# return a list of users
			pass
		else:
			# expose a single user
			pass

	def post(self):
		# create a new user
		pass

	def delete(self, username):
		# delete a single user
		pass

	def put(self, username):
		# update a single user
		pass
		
		
		

@app.route('/', methods=['GET'])
def index() :
	if session.get('join_code') is not None:
		return 'you are already a part of: ' + session['join_code']
	return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
	# need to check if join code is valid and add user to that event

	session['join_code'] = request.form['join_code']
	return render_template('testing.html')

@app.route('/userprofile', methods=['GET'])
def userprofile() :
	return render_template('testing.html')
	  
@app.route('/submit_form',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		print(result)
		return 'form submitted'
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique = False)
	firstName = db.Column(db.String(80), unique = False, nullable = True)
	eid = db.Column(db.Integer)
	# age = db.Column(db.Integer, unique = False, nullable = True)
	# profilePic = db.Column(db.LargeBinary, unique = True, nullable = True, required=False)
	# email = db.Column(db.String(120), unique=True, nullable=True, required=False)
	# passions = db.Column(db.String(80), unique = False, nullable = True,required=False)
	# hometown = db.Column(db.String(80), unique = False, nullable = True, required=False)
	# bio = db.Column(db.String(300), unique = False, nullable = True, required=False)
	
	

	def __repr__(self):
		return '<User %r>' % self.username
		
class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=False)
	joincode = db.Column(db.String(80), unique=True)

class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	eid = db.Column(db.Integer)
	liker = db.Column(db.Integer)
	likee = db.Column(db.Integer)
	rating = db.Column(db.String(80))

class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	eid = db.Column(db.Integer)
	first = db.Column(db.Integer)
	second = db.Column(db.Integer)
	color = db.Column(db.String(80))

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
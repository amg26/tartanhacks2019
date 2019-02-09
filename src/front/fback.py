from flask import Flask, request, render_template, session
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from database import User, Event, db

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'slqclkekql-12cumiojkwfa-fo2i4c2ic4flajkfa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''Add database'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test5.db'

with app.app_context():
	db.init_app(app)
	db.create_all()
	db.session.add(Event(name="testevent", joincode="hello"))
	db.session.commit()

@app.route('/', methods=['GET'])
def index():
	usr = User(username="testuser2", firstName="test")

	db.session.add(usr)
	print(usr.id)
	db.session.commit()
	print(usr.id)

	print(User.query.all())

	if session.get('join_code') is not None:
		pass
		#return 'you are already a part of: ' + session['join_code']
	return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
	# need to check if join code is valid and add user to that event
	ev = db.session.query(Event).filter(Event.joincode == request.form['join_code']).first()

	if ev is not None:
		print("that's valid my lad")
		render_template('testing.html')
	else:
		return 'INVALID JOIN CODE'

	session['join_code'] = request.form['join_code']
	return render_template('testing.html')

@app.route('/userprofile', methods=['GET'])
def userprofile() :
	return render_template('testing.html')

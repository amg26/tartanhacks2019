from flask import Flask, request, render_template, session, jsonify, redirect
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
import os
from database import User, Event, Rating, Match, db
import match

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'slqclkekql-12cumiojkwfa-fo2i4c2ic4flajkfa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "user_uploads"

'''Add database'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #'sqlite:////tmp/test10.db'

with app.app_context():
	db.init_app(app)
	print('hello')
	db.create_all()
	#db.session.add(Event(name="testevent", joincode="hello"))
	db.session.commit()

@app.route('/', methods=['GET'])
def index():
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
	  
@app.route('/submit_form',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		ev = db.session.query(Event).filter(Event.joincode == session['join_code']).first()
		usr = User(username=request.form['name_form'],
			firstName=request.form['name_form'],
			eid=ev.id,
			age=request.form['age_form'],
			langy=request.form['language_form'],
			idea=request.form['idea_form'],
			exp=request.form['exp_form'],
			plant=request.form['plant_form'],
			)
		db.session.add(usr)
		db.session.commit()
		print('added ' + str(usr))
		session['uid'] = usr.id
		return render_template('waiting.html')

@app.route('/rate', methods=['GET'])
def rate():
	rating_user = db.session.query(User).filter(User.id == session['uid']).first()

	next_uid = match.next(db, rating_user)
	if next_uid is not None:
		usr = db.session.query(User).filter(User.id == match.next(db, rating_user)).first()
		return render_template('rateuser.html', firstName=usr.firstName, userid=usr.id, age=usr.age, langy=usr.langy, idea=usr.idea, exp=usr.exp, plant=usr.plant)
	else:
		return render_template('waiting.html')		#TODO: replace with a template or something

@app.route('/like/<int:userid>', methods=['POST'])
def like(userid):
	liker = db.session.query(User).filter(User.id == session['uid']).first()
	likee = db.session.query(User).filter(User.id == userid).first()

	if likee is None or liker is None:
		return 'bad'

	if likee.eid != liker.eid:
		return 'bad'

	unique_check = db.session.query(Rating).filter(Rating.likee == likee.id, Rating.liker == liker.id).first()
	if unique_check is not None:
		# this is a duplicate like, ignore it
		pass
	else:
		rating = Rating(eid = liker.eid, liker=liker.id, likee=likee.id, rating='like')
		print("adding like for " + str(rating))
		db.session.add(rating)
		db.session.commit()

	next_uid = match.next(db, liker)
	if next_uid is not None:
		next_usr = db.session.query(User).filter(User.id == next_uid).first()
		return jsonify({'userid': next_uid, 'firstName': next_usr.firstName})
	else:
		return jsonify({'userid': -1})		#TODO: replace with a template

@app.route('/dislike/<int:userid>', methods=['POST'])
def dislike(userid):
	liker = db.session.query(User).filter(User.id == session['uid']).first()
	likee = db.session.query(User).filter(User.id == userid).first()

	if likee is None or liker is None:
		return 'bad'

	if likee.eid != liker.eid:
		return 'bad'

	unique_check = db.session.query(Rating).filter(Rating.likee == likee.id, Rating.liker == liker.id).first()
	if unique_check is not None:
		# this is a duplicate dislike, ignore it
		pass
	else:
		rating = Rating(eid = liker.eid, liker=liker.id, likee=likee.id, rating='dislike')
		print("adding like for " + str(rating))
		db.session.add(rating)
		db.session.commit()
	return jsonify({'userid': match.next(db, None)})

@app.route('/match', methods=['GET'])
def view_match():
	usr = db.session.query(User).filter(User.id == session['uid']).first()
	m = match.get_user_match(db, usr.id)

	if m is None:
		# couldn't find match
		return redirect('/rate')

	other = m.first
	if usr.id == other:
		other = m.second
	o_usr = db.session.query(User).filter(User.id == other).first()

	return render_template('match.html', user1=usr, user2 = o_usr, bg_color=m.color)

@app.route('/match/check', methods=['POST'])
def post_match_check():
	usr = db.session.query(User).filter(User.id == session['uid']).first()
	if usr is None:
		return 'no user session'
	rate = match.next(db, usr)
	if rate is None:
		rate = False
	else:
		rate = True

	return jsonify({'match': match.is_user_matched(db, usr.id), 'rate': rate})

@app.route('/event/create', methods=['GET'])
def view_create():
	return render_template('create.html')

@app.route('/event/create', methods=['POST'])
def post_create():
	ev_unique_check = db.session.query(Event).filter(Event.joincode == request.form['join_code']).first()
	if ev_unique_check is not None:
		return 'That join code has already been used.'

	ev = Event(name=request.form['event_name'], joincode=request.form['join_code'])
	db.session.add(ev)
	db.session.commit()

	session['event_creator'] = True
	session['event_id']  = ev.id

	return redirect('/event/view/' + str(ev.id))

@app.route('/event/view/<int:id>', methods=['GET'])
def view_event(id):
	ev = db.session.query(Event).filter(Event.id == id).first()
	if ev is None:
		return 'bad id'

	return render_template('event.html', name=ev.name, joincode=ev.joincode)

@app.route('/event/num_users', methods=['POST'])
def event_num_users():
	if not session['event_creator']:
		return 'bad'

	num_users = db.session.query(User).filter(User.eid == session['event_id']).count()
	print(num_users)
	print(session['event_id'])

	return jsonify({'num_users': num_users})

@app.route('/event/generate', methods=['POST'])
def event_generate_groups():
	if not session['event_creator']:
		return 'bad'

	ev = db.session.query(Event).filter(Event.id == session['event_id']).first()

	match.generate_matches(db, ev.id)

	return 'ok'

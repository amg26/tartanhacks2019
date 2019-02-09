from database import User, Event, Rating
from sqlalchemy import or_

def next(db, user):
	# Get other users in our event
	users = db.session.query(User).filter(User.eid == user.eid, User.id != user.id).all()

	if len(users) == 0:
		#there are no users left to rate
		return None

	for usr in users:
		print(usr)
		rating = db.session.query(Rating).filter(Rating.likee == usr.id, Rating.liker == user.id).first()
		if rating is None:
			return usr.id

	# we have rated all users in this case
	return None

def get_match(db, uid, uid2):
	if uid > uid2:
		tmp = uid
		uid = uid2
		uid2 = tmp

	match = db.session.query(Match).filter(Match.first == uid, Match.second == uid2).first()
	
	return match

def are_mutually_liked(db, ev, uid, uid2):
	r1 = db.session.query(Rating).filter(Rating.eid == ev, liker == uid, likee == uid2).first()
	r1 = db.session.query(Rating).filter(Rating.eid == ev, liker == uid, likee == uid2).first()

	return (r1 is not None) and (r2 is not None)

def is_user_matched(db, uid):
	match = match = db.session.query(Match).filter(or_(Match.first == uid, Match.second == uid)).first()

	return match is not None

def create_match(db, eid, uid, uid2):
	if uid > uid2:
		tmp = uid
		uid = uid2
		uid2 = tmp

	match = Match(eid=eid, first=uid, second=uid2)
	db.session.add(match)
	db.session.commit()


def generate_matches(db, eid):
	event = db.session.query(Event).filter(Event.id == eid).first()

	users = db.session.query(User).all()

	for user in users:
		if not is_user_matched(db, user.id):
			# iterate through all users in this event and try to match them
			other_users = db.session.query(User).filter(User.eid == eid, User.id != user.id)

			for o_user in other_users:
				if not is_user_matched(db, o_user.id):
					if are_mutually_liked(db, event.eid, user.id, o_user.id):
						create_match(db, event.id, user.id, o_user.id)
						# we matched, get out of here
						break

from database import User, Event, Rating

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
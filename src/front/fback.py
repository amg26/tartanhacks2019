from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='/static')


'''Add database'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)




class User(db.Model):
	username = db.Column(db.String(80), primary_key=True)
	firstName = db.Column(db.String(80), unique = False, nullable = False)
	age = db.Column(db.Integer, unique = False, Nullable = True)
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
	return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
	return 'nice ' + request.form['join_code']

@app.route('/userprofile', methods=['GET'])
def userprofile() :
	return render_template('testing.html')

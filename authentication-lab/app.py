from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
config= {
  "apiKey": "AIzaSyBcjUHeornT6_yxiUol9-NNJJws8agscaQ",
  "authDomain": "y2-summer-firstproject.firebaseapp.com",
  "projectId": "y2-summer-firstproject",
  "storageBucket": "y2-summer-firstproject.appspot.com",
  "messagingSenderId": "304837708877",
  "appId": "1:304837708877:web:9bf36b3851550923a7a004",
  "measurementId": "G-QZN6JHME5E",
  "databaseURL":"https://y2-summer-firstproject-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase= pyrebase.initialize_app(config)
auth= firebase.auth()
db= firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
	error= ""
	if request.method=="POST":
		email= request.form['email']
		password=request.form['password']
		try:
			login_session['user']= auth.create_user_with_email_and_password(email,password)
			user={"email": request.form['email'],
			"password": request.form['password'],
			"username": request.form['username'],
			"fullname": request.form['fullname'],
			"bio": request.form['bio']
			}
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('add_tweet'))
		except:
			error="Authentication Failed"
	return render_template('signup.html')

	

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
		   error = "Authentication failed"
	return render_template("signin.html")

	


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	error= ""
	if request.method=="POST":
		# try:
		tweet={"title": request.form['title'],
		"text": request.form['text'],
		"imagelink": request.form['imagelink'],
		"uid": login_session['user']['localId']}
		db.child("Tweets").push(tweet)
		return redirect(url_for('all_tweets'))
		# except:
		# 	print("couldn't add tweet")
	return render_template("add_tweet.html")



@app.route('/tweets', methods=['GET', 'POST'])
def all_tweets():
	tweets= db.child('Tweets').get().val()
	return render_template('tweets.html', tweets=tweets)

# return render_template("tweets.html")



if __name__ == '__main__':
	app.run(debug=True)
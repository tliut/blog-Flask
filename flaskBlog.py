from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from forms import RegistrationForm, LoginForm
app = Flask(__name__)

# Use secrets module in python "secrets.token_hex(16) to generate a random secret"
app.config['SECRET_KEY'] = 'af475c5067b73cd007dbc8805acfc201'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:password@tl-test-mysql.cs3minrzf996.us-east-2.rds.amazonaws.com/flaskBlogDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    
posts = [
    {
        'author': 'Tony Liu',
        'title':    'Blog Post 1',
        'content':  'First Post Content',
        'date_posted':  'Oct 25, 2020'
    },
    {
        'author': 'Vivian Liu',
        'title':    'Blog Post 2',
        'content':  'Second Post Content',
        'date_posted':  'Oct 25, 2020'
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts= posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template('login.html', title='login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
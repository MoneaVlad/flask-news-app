from news_app.news import getNewsFromTopic, getTopics
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from news_app import app, db
from news_app.forms import RegistrationForm, LoginForm
from news_app.news import getNewsFromTopic, getTopics
from news_app.models import User, UserSchema



@app.route("/")
@app.route("/home")
def home():
    """
    Define the home page elements
    """
    return render_template("home.html")


@app.route("/news", methods = ["GET", "POST"] )
@login_required
def news():
    """
    Accepts both GET and POST requests. If it's a GET request,
    you wouldn't have a last selected thing, so it's set to an
    empty string. If it's a POST request, we fetch the selected
    thing and return the same template with the pre-selected
    thing.
    """
    selectedNewsSection = ''
    topics = getTopics()
    if request.method == "GET":
        # Render just the template when method is "GET"
        return render_template ( "hotNews.html", topics = topics  )

    if request.method == "POST":
        selectedNewsSection = request.form["newsSection"]
        news = getNewsFromTopic(selectedNewsSection)

        return render_template( "hotNews.html" , \
                                topics = topics, \
                                selectedNewsSection = selectedNewsSection, \
                                result = news \
                            )

@app.route("/register", methods = ['GET', 'POST'])
def register():
    """
    Function to register an user
    """
    if current_user.is_authenticated:
        return redirect(url_for('news'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('The account was created successfully!', 'success')
            return redirect(url_for('login'))
        except:
            flash('The email is already used!', 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    """
    Function to login an user
    """
    if current_user.is_authenticated:
        return redirect(url_for('news'))
    form = LoginForm()
    if form.validate_on_submit():
        user = None
        try:
            user = User.query.filter_by(email=form.email.data).first()
        except:
            print ("Couldn't find the login email")

        if user and user.password == form.password.data:
            login_user(user, remember=None)
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('news'))
        else:
            flash('Wrong credentials!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    """
    Function to log out an user
    """
    logout_user()
    return redirect(url_for('home'))
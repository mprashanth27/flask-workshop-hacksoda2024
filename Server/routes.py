# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from model import User  # Import User model from models.py
from db import db  # Import db from extensions.py
from forms import LoginForm, SignupForm  # Import form classes from forms.py

# Create a Blueprint for organizing routes separately from the main application instance
app = Blueprint('main', __name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the home page template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()  # Initialize the signup form
    
    if form.validate_on_submit():  # Check if form submission is valid (POST request)
        print("Signup form submitted and validated.")
        user = User(username=form.username.data, password=form.password.data)  # Create a new User object
        
        # Add the new user to the session for insertion into the database
        try:
            db.session.add(user)
            db.session.commit()
            print(f"User {user.username} added to the database.")
            
            # Store the username in the session
            session['username'] = user.username
            
            flash('Signup successful! You can now login.', 'success')  # Flash success message to user
            
            return redirect(url_for('main.welcome'))  # Redirect to welcome page after successful signup
        except Exception as e:
            db.session.rollback()  # Rollback in case of any error
            print(f"Error adding user: {e}")
            flash('An error occurred. Please try again.', 'danger')

    print("Rendering signup page.")
    return render_template('signup.html', form=form)  # Render signup form template if GET request or validation fails

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Initialize the login form
    
    if form.validate_on_submit():  # Check if form submission is valid (POST request)
        print("Login form submitted and validated.")
        user = User.query.filter_by(username=form.username.data).first()  # Query database for user by username
        
        if user:
            print(f"User found: {user.username}")
        else:
            print("User not found.")
        
        if user and user.password == form.password.data:  # Validate password (should be hashed in a real app)
            # Store the username in the session
            session['username'] = user.username
            flash('Login successful!', 'success')  # Flash success message to user
            print('Login successful! Redirecting to welcome page.')
            
            return redirect(url_for('main.welcome'))  # Redirect to welcome page after successful login

        else:
            flash('Login failed. Check your username and password.', 'danger')  # Flash error message on failure
            print("Login failed. Username or password incorrect.")

    print("Rendering login page.")
    return render_template('login.html', form=form)  # Render login form template if GET request or validation fails

@app.route('/welcome')
def welcome():
    username = session.get('username')  # Get the username from the session
    if not username:
        flash('You are not logged in. Please login first.', 'warning')
        return redirect(url_for('main.login'))  # If not logged in, redirect to login page
    
    print(f"Welcome page accessed by {username}")
    return render_template('welcome.html', username=username)  # Render the welcome template


'''
user 1 : soda, pw:1234
'''
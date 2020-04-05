from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)                            # Blueprints 


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')                              # decode('utf-8'), gives us a String instead of byte codes, hashing the plain-text password from user input in the forms, and storing it in a variable
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)                        # So take the user input from the forms and password variables and past it into the user 
        db.session.add(user)                                                                                             # Add user to the database.db
        db.session.commit()                                                                                              # Commit changes in database.db
        flash(f'Welcome {form.username.data}! Your account has been created! You are now able to log in!', 'success')    # Display success message! For anyone wondering 'success' is just a bootstrap class, it gives a green-ish hue. 
        return redirect( url_for('users.login') )                                                                        # Redirect to Login page

    return render_template('register.html', title='Register', form=form)



@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))                                               # Redirect to home page -- Prevent's already logged in user's from logging in again! 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()                          # Look for user email in db, and stre it 
        if user and bcrypt.check_password_hash(user.password, form.password.data):          # If the provided email exists AND Password Hash matches with user input from the form
            login_user(user, remember=form.remember.data)                                   # login_user is part of flask_login, and like UserMixin it's really useful, it accepts two paramters, the user object, and the remember form data which is a boolean
            next_page = request.args.get('next')                                            # using .get prevents us from getting a null pointer exception
            return redirect(next_page) if next_page else redirect(url_for('main.home'))     # If the next page exists redirect to the next page, if it doesn't exist redirect to Home page
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')       # For anyone wondering 'danger' is just a bootstrap class, it gives a red-ish/pink-ish hue for an error message                           
    return render_template('login.html', title='Login', form=form)



@users.route('/logout')
def logout():                                                                               # The logout function is pretty simple it uses the flask-login method, and redirects the user to the home page as a Guest User
    logout_user()                                                                           # logout_user is part of flask-login, and like UserMixin it's reallu useful, it implicitly knows who's logged in, and does not accept any parameters!
    return redirect(url_for('main.home'))                                                   # Redirect to Home page 

    # Confession time: In some of my projects I would log people out by redirecting them to the log in page! 
    # This is VERY VERY insecure, and dumb as your not actually deleting their cookies and ending there session! O_O 
    # The nice thing is that flask handle's all of that for you here! :D 


@users.route('/account', methods=['GET', 'POST'])
@login_required                                                                             # login_required is part of flask-login, and like UserMixin it's really useful, this can essentially prevent IDOR! Insecure Direct Object References 
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data                                          # This is a SQLAlchemy perk it allows us to take the current_user data which we get thanks to flask_login, and then overwrites it with the form data the user submits!
        current_user.email = form.email.data                                                # So over here we're overwriting the current_user email with the email the user submits in the form!
        db.session.commit()                                                                 # Commit changes in database.db
        flash('Your account has been updated!', 'success')                                  # Display success message! For anyone wondering 'success' is just a bootstrap class, it gives a green-ish hue.
        return redirect(url_for('users.account'))                                           # Redirect to account, without this line of code, the broswer on the redirect below would send multiple post requests causing some problems
    elif request.method == 'GET':
        form.username.data = current_user.username                                          # This populates the username field upon a 'GET' request
        form.email.data = current_user.email                                                # This populates the email field upon a 'GET' request
    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)



@users.route('/user/<string:username>')                                       # String  
def user_posts(username):                                                                                                          
    page = request.args.get('page', 1, type=int)                            # We request a page, the default page is 1, of type int
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)                                    
                                                                            # Okay this was tough, getting ES6 promises PTSD! phew ... This is essentially the same query as the 'main.home' route BUT this time  
                                                                            # We are filtering the query by date posted, ensuring it's still paginated, but now we've added another filter to look for posts made from a spedific user. 
    return render_template('user_posts.html', posts=posts, user=user)       # Redirect to user_posts.html

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
    
from flaskblog import db,bcrypt
from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request, abort
from flaskblog.modle import User, Post
from flaskblog.users.form import (RegistrationForm, LoginForm, AccountUpdateForm,
                             RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_tokenmessage_url
from flask_login import login_user, login_required, logout_user, current_user


users_r = Blueprint('users', __name__)

# LOGIN
@users_r.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))

  form = LoginForm()
  if form.validate_on_submit():
    have_user = User.query.filter_by(email=form.email.data).first()
    if have_user and bcrypt.check_password_hash(have_user.password, form.password.data):
      login_user(have_user, remember=form.remember.data)
      next_page = request.args.get('next')
      if next_page:
        return redirect(next_page)
      else:
        return redirect(url_for('main.home'))
    else:
      flash('Login Failed Check your Email and password','danger')

  return render_template('login.html', title='Login', form=form)

# REGISTER
@users_r.route('/register', methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash("Account Created Successfully!. Now you able to login", 'success')
    return redirect(url_for('users.login'))

  return render_template('register.html', title='Registration', form=form)


# LOGOUT
@users_r.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.home'))




# USER ACCOUNT
@users_r.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = AccountUpdateForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.img_file = picture_file
      
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your Account Information Updated', 'success')
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    
  image_file_url = url_for('static', filename='images/'+ current_user.img_file)
  return render_template('account.html', title="Account", image_file_url = image_file_url, form = form)


# USER_POSTS
@users_r.route('/user/<string:username>')
def user_posts(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  posts = Post.query.filter_by(author=user)\
         .order_by(Post.post_date.desc())\
         .paginate(page=page, per_page=2)
  return render_template('user_posts.html', user=user, posts=posts)



#REQUEST RESET PASSWORD
@users_r.route('/req_reset_password', methods=['GET','POST'])
def req_reset_password():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_tokenmessage_url(user)
    flash("An email has been sent with instruction to reset your password", "info")
    return redirect(url_for('users.login'))
  return render_template('req_reset_password.html', title='Request Reset Password', form=form)


#RESET PASSWORD
@users_r.route('/req_reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))

  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an invalid or expired token', 'warning')
    return redirect(url_for('users.req_reset_password'))

  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    user.password = hashed_password
    db.session.commit()
    flash('Your password has been updated!. now you able to login', 'success')
    return redirect(url_for('users.login'))
  return render_template('reset_password.html', title='Reset Password', form=form)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flaskblog.modle import Post

main = Blueprint('main', __name__)

# HOME PAGE
@main.route('/')
@main.route('/home')
def home():
  page = request.args.get('page', 1, type=int)
  post_data = Post.query.order_by(Post.post_date.desc()).paginate(per_page=2, page=page)
  return render_template('home.html', title='Home', posts=post_data)


# ABOUT PAGE
@main.route('/about')
def about():
  return render_template('about.html', title='About')

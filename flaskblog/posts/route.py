from flaskblog import db
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flaskblog.modle import Post
from flaskblog.posts.form import NewPostForm
from flask_login import login_required,current_user

posts = Blueprint('posts', __name__)

# NEW POST
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
  form = NewPostForm()
  if form.validate_on_submit():
    new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(new_post)
    db.session.commit()
    flash('Your Post Published!', 'success')
    return redirect(url_for('main.home'))
  return render_template('new_post.html', btn_text='Post', title='New Post', legend='New Post', form=form)


# SINGLE POST
@posts.route('/post/<int:post_id>')
def single_post(post_id):
  from_u_p_page = request.args.get('from_u_p_page') # for redirect user posts page if come form user_post page
  single_post = Post.query.get_or_404(post_id)
  return render_template('single_post.html', title=single_post.title, post=single_post, from_u_p_page=from_u_p_page)


# UPDATE POSTS
@posts.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
  post_data = Post.query.get_or_404(post_id)
  if post_data.author != current_user:
    abort(403)
  form = NewPostForm()
  if form.validate_on_submit():
    post_data.title = form.title.data
    post_data.content = form.content.data
    db.session.commit()
    flash('Your Post Has Been Updated!', 'success')
    return redirect(url_for('posts.single_post', post_id=post_data.id))

  elif request.method == 'GET':
    form.title.data = post_data.title
    form.content.data = post_data.content

  return render_template('new_post.html', btn_text='Update', title='Update Post', legend="Update Post", form=form)


# DELETE POSTS
@posts.route('/post/<int:post_id>/delete_post', methods=['POST'])
@login_required
def delete_post(post_id):
  from_u_p_page = request.args.get('from_u_p_page') # for redirect user posts page if come form user_post page
  post_data = Post.query.get_or_404(post_id)
  if post_data.author != current_user:
    abort(403)
  db.session.delete(post_data)
  db.session.commit()
  flash('Your Post Has Been Deleted!', 'success')
  if from_u_p_page:
    return redirect(url_for('posts.user_posts', username=post_data.author.username))
  return redirect(url_for('main.home'))

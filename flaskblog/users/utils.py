import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message

# RESIZE AND SAVE IMAGE
def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  f_name, f_ext =  os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
  
  # form_picture.save(picture_path) #nomarl save
  
  #pillow resize and save
  output_size = (125,125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)
  
  return picture_fn




def send_tokenmessage_url(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request',
                sender='nursaykat@gmail.com',
                recipients=[user.email])
  msg.body = f'''To reset your password, visit the flowing link:
{url_for('users.reset_token', token=token, _external=True)} 
  
  If you did not make this request then simply ignore this email and no change
  '''
  #_external=True // for absulate path
  mail.send(msg) # message and link : this link with token and absulate path

import os

class Configuration:
    SECRET_KEY = os.environ.get('MY_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('MY_DB')

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MY_EMAIL')
    MAIL_PASSWORD = os.environ.get('MY_EMAIL_APP_PASS')
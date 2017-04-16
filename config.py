import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zlc19910213@localhost/test'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'conoswinagain'

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'czyuwei@gmail.com'
MAIL_PASSWORD = 'yw19880702'
CONOS_MAIL_SUBJECT_PREFIX = '[Conos]'
CONOS_MAIL_SENDER = 'Conos Admin <admin@conos.com>'

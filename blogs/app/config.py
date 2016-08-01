import os

class Configuration(object):
  DEBUG = True

  APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
  SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/blog.db' % APPLICATION_DIR
  # Flask-SQLAlchemy's event system - he thong nay ko tot/ko nhieu nguoi xai, nen tat/OFF di
  # Neu ko tat, thi khi run scripts se bao warning
  SQLALCHEMY_TRACK_MODIFICATIONS = False

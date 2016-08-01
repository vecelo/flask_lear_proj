from flask import Flask
### trong sach dung from flask.ext.sqlalchemy import SQLAlchemy --- bao loi. Nen dung nhu ben duoi (line 3).
### neu ca 2 lenh deu ko duoc, thi dung 'pip install Flask-SQLAlchemy==1.0
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy
from config import Configuration

# trong sach dung from flask.ext.migrate va flask.ext.script nhung bao loi. Nen dung kieu moi, ko co thi dung 'pip install flask_migrate' de down ve
from flask_migrate import Migrate, MigrateCommand # Migrate dung de update database
from flask_script import Manager # method Manager cua package flask_script dung de execute command tu cmdline


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

# su dung cac function cua MIGRATE cho app
migrate = Migrate(app, db)

# dung method Manager de execute cac cmd cua MIGRATE
manager = Manager(app)
manager.add_command('db', MigrateCommand)
from flask import Flask
app = Flask(__name__)

from flask.ext.sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./gamedatabase.db'
db = SQLAlchemy(app)

import mainapp.api.models
db.create_all()


import mainapp.api.views

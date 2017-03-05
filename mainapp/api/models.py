from mainapp import db

import hashlib

# Default responses
OK_RESPONSE = {}
OK_RESPONSE['response'] = 'success'

ERROR_RESPONSE = {}
ERROR_RESPONSE['response'] = 'fail'
ERROR_RESPONSE['info'] = 'Unknown issue'

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    iaCode = db.Column(db.Text)

    def __init__(self, name, password):
        m = hashlib.md5()
        m.update(password)
        password_hashed = m.hexdigest()
        self.iaCode = 'return direction'

        self.name = name
        self.password = password_hashed

    def __repr__(self):
        return '<Player %d>' % self.id

    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'name': self.name,
       }
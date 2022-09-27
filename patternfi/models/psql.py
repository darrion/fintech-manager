from flask import current_app
from sqlalchemy.dialects import postgresql
from constants import DECIMAL_PRECISION, INTEGER_PRECISION

db = current_app.db

class Client(db.Model):
    
    """A client of the firm."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    owned_accounts = db.relationship('models.psql.Account', backref='client_ref', cascade="all, delete")

    advisor_id = db.Column(db.Integer, db.ForeignKey('advisor.id'))

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.__dict__[k] = v
    
    def json(self):
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Advisor(db.Model):
    
    """An advisor to clients of the firm."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    specializations = db.relationship(
        'models.psql.Specialization', 
        backref='specialization_advisor_ref', 
        cascade="all, delete"
        )

    clients = db.relationship(
        'models.psql.Client', 
        backref='client_advisor_ref', 
        cascade="all, delete"
        )

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.__dict__[k] = v
    
    def json(self):
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Specialization(db.Model):

    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    focus = db.Column(db.String())
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisor.id'))

class Account(db.Model):

    """A brokerage account at the firm."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(INTEGER_PRECISION, DECIMAL_PRECISION))
    account_type = postgresql.ENUM("brokerage", "ira", name="type", nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey(Client.id))

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.__dict__[k] = v

    def json(self):
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}

from models.psql import Account
from flask import current_app as app 
from datetime import datetime
from decorators import transaction

def create(**kwargs):

    with transaction():
        (
            app
            .db
            .session
            .add(Account(
                **kwargs
            ))
        )
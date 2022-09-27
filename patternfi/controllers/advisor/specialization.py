from flask import current_app as app 
from models.psql import Specialization
from decorators import transaction


def add(**kwargs):
    with transaction():
        (
            app
            .db
            .session
            .add(Specialization(**kwargs))
        )
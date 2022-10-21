from flask import current_app as app
from models.psql import Client, Account, Advisor
from constants import AccountType
from decorators import transaction

db = app.db

def get(client_id: str):

    client_id = int(client_id)
    return app.db.session.query(Client).filter(Client.id == client_id).first()

def add(**kwargs):
    
    client = Client(**kwargs)
    (
        app
        .db
        .session
        .add(client)
    )
    app.db.session.flush()
    app.db.session.refresh(client)
    return client.id

def get_brokerage_accounts(client_id: int):

    accounts = []

    with transaction():
        accounts = (
            app
            .db
            .session
            .query(Account)
            .filter(Account.client_id == client_id)
            .filter(Account.type == AccountType.BROKERAGE.value)
            .all()
        )
    
    return accounts


def get_retirement_accounts(client_id):
    return (
        app
        .db
        .session
        .query(Account)
        .filter(Account.client_id == client_id)
        .filter(Account.type == AccountType.IRA.value)
        .all()
    )

def get_all_accounts(client_id):
    return (
        app
        .db
        .session
        .query(Account)
        .filter(Account.client_id == client_id)
        .all()
    ) 

def get_advisor(client_id):
    return (
        app
        .db
        .session
        .query(Advisor)
        .join(Client)
        .filter(Client.id == client_id)
        .filter(Client.advisor == Advisor.id)
        .first()
    )
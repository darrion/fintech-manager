
import re
from . import specialization
from errors import ApiError

from flask import current_app as app
from models.psql import Client, Advisor, Account
from datetime import datetime

from decorators import transaction

db = app.db

def get(advisor_id: str):

    advisor_id = int(advisor_id)
    return app.db.session.query(Advisor).filter(Advisor.id == advisor_id).first()

def add(**kwargs):
    
    advisor = Advisor(**kwargs)
    (
        app
        .db
        .session
        .add(advisor)
    )
    app.db.session.flush()
    app.db.session.refresh(advisor)
    return advisor.id

def assign(advisor_id: str, client_id: str):

    advisor = get(advisor_id=advisor_id)

    if not advisor:
        raise ApiError(f"No advisor with id {advisor_id} exists.")

    advisor_id = int(advisor_id)
    client_id = int(client_id)
    
    with transaction():
        (
            app
            .db
            .session
            .query(Client)
            .filter(Client.id == client_id)
            .update({
                "advisor_id": advisor_id
            })
        )
        

def dismiss(client_id: int):
    
    with transaction():
        (
            app
            .db
            .session
            .query(Client)
            .filter(Client.id == client_id)
            .update({
                "advisor_id": None, 
                "updated_at": datetime.now()
            })
        )

def get_assigned_clients(advisor_id: int, page: int, limit: int):   
    
    from sqlalchemy.sql import func

    def float_or_none(value):
        if value is None: 
            return 0
        else:
            return float(value)

    paginated_results = (
        app.db.session.query(Client, func.sum(Account.value))
        .join(Account, isouter=True)
        .filter(Client.advisor_id == advisor_id)
        .group_by(Client.id)
        .paginate(page=page, per_page=limit)
    )

    items = paginated_results.items
    total = int(paginated_results.total)
    clients = list(map(lambda item: {"client": item[0].json(), "value": float_or_none(item[1])}, items))
    return total, clients

def get_available_advisors(page: int, limit: int):
    
    paginated_advisors = (
        app
        .db
        .session
        .query(Advisor)
        .paginate(page=page, per_page=limit)
    )

    advisors = paginated_advisors.items
    total = int(paginated_advisors.total)
    advisors = list(map(lambda advisor: advisor.json(), advisors))
    return total, advisors
   
    
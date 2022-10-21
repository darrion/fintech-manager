import os
import pytest
import flask

@pytest.fixture(scope="session")
def app():

    app = flask.Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI_TEST']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app 

@pytest.fixture(scope="session")
def db_session(app):

    with app.app_context():
        
        from flask_sqlalchemy import SQLAlchemy

        db = SQLAlchemy(session_options={'autoflush': False})
        db.init_app(app)

        setattr(app, "db", db)
        
        import models
        app.db.create_all()
        
        yield db.session

        db.drop_all() ### Clean up

@pytest.fixture(scope="session")
def client(app):

    return app.test_client()

def test_add_client(app, db_session):

    """Add a client and verify."""

    with app.app_context():

        from models.psql import Client
        from controllers import client

        first_name = 'Darrion'
        last_name = 'Banks'
        
        client_id = client.add(**{
            'first_name': first_name, 
            'last_name': last_name, 
            
        })

        result = db_session.query(Client).filter(
                Client.first_name == first_name, 
                Client.last_name == last_name
            ).first()

        assert result is not None
        assert result.id == client_id

def test_add_advisor(app, db_session):

    """Add an advisor and verify."""

    with app.app_context():

        from models.psql import Advisor
        from controllers import advisor

        first_name = 'Xinran'
        last_name = 'Wang'
        
        advisor_id = advisor.add(**{
            'first_name': first_name, 
            'last_name': last_name, 
            
        })

        result = db_session.query(Advisor).filter(
                Advisor.first_name == first_name, 
                Advisor.last_name == last_name
            ).first()

        assert result is not None
        assert result.id == advisor_id

def test_get_available_advisors(app, db_session):

    """Return all advisors in database."""

    with app.app_context():

        from controllers import advisor
        from models.psql import Advisor
        
        db_session.add(Advisor(**{
            'first_name': 'Marco', 
            'last_name': 'Inaros', 
        }))

        db_session.add(Advisor(**{
            'first_name': 'Theresa', 
            'last_name': 'Yao', 
        }))

        db_session.commit()

        total, advisors = advisor.get_available_advisors(page=1, limit=10)

        assert total == 2

def test_assign_advisor(app, db_session):

    """Assign an advisor to a client and validate foreign key."""

    with app.app_context():

        from models.psql import Advisor, Client
        import controllers

        client = {
            'first_name': 'Chrisjen',
            'last_name': 'Avasarala'
        }

        advisor = {
            'first_name': 'James', 
            'last_name': 'Holden', 
        }

        client = Client(**client)
        advisor = Advisor(**advisor)

        db_session.add(client)
        db_session.add(advisor)

        db_session.flush()
        
        db_session.refresh(client)
        db_session.refresh(advisor)

        client_id = client.id 
        advisor_id = advisor.id

        controllers.advisor.assign(advisor_id, client_id)

        client = db_session.query(Client).filter(Client.id == client_id).first()

        assert client.advisor_id == advisor_id

def test_get_clients(app, db_session):

    """Get clients of advisor and assert sum of account values is correct."""

    with app.app_context():

        from models.psql import Advisor, Client, Account
        import controllers

        expected_total_clients = 4

        advisor = Advisor(**{
                'first_name': 'Chrisjen',
                'last_name': 'Avasarala',
        })

        c1 = Client(**{
            'first_name': 'James', 
            'last_name': 'Holden', 
        })

        c1_acct1_value = 1000000
        c1_acct2_value = 55656

        c2 = Client(**{
            'first_name': 'Amos', 
            'last_name': 'Burton', 
        })

        c3 = Client(**{
            'first_name': 'Roberta', 
            'last_name': 'Draper', 
        })

        c4 = Client(**{
            'first_name': 'Sadavir', 
            'last_name': 'Errinwright', 
        })

        db_session.add(advisor)
        db_session.add(c1)
        db_session.add(c2)
        db_session.add(c3)
        db_session.add(c4)

        db_session.flush()

        db_session.refresh(advisor)
        db_session.refresh(c1)
        db_session.refresh(c2)
        db_session.refresh(c3)
        db_session.refresh(c4)

        (
            db_session
            .query(Client)
            .filter(Client.id == c1.id)
            .update({
                "advisor_id": advisor.id
            }))

        (
            db_session.query(Client)
            .filter(Client.id == c2.id)
            .update({
                "advisor_id": advisor.id
            }))
        (
            db_session.query(Client)
            .filter(Client.id == c3.id)
            .update({
                "advisor_id": advisor.id
            }))
        (
            db_session.query(Client)
            .filter(Client.id == c4.id)
            .update({
                "advisor_id": advisor.id
            }))

        db_session.add(Account(**{
            'value': c1_acct1_value, 
            'client_id': c1.id,
        }))

        db_session.add(Account(**{
            'value': c1_acct2_value, 
            'client_id': c1.id,
        }))

        db_session.commit()

        total_clients, results = controllers.advisor.get_assigned_clients(advisor.id, page=1, limit=10)   
        
        c1_acct_sum = c1_acct1_value + c1_acct2_value
        client_c1 = dict(*filter(
                lambda 
                item: item['client']['first_name'] == 'James' 
                and item['client']['last_name'] == 'Holden',
                results
                ))
        

        account_values = [*filter(lambda item: 'value' in item, results)]
        positive_account_values = [*filter(lambda item: item['value'] > 0, account_values)]
        zero_account_values = [*filter(lambda item:item['value'] == 0, account_values)]

        assert len(account_values) == expected_total_clients == total_clients
        assert len(positive_account_values) == 1
        assert len(zero_account_values) == 3
        assert client_c1['value'] == c1_acct_sum
    
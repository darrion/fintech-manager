from contextlib import contextmanager
from flask import current_app

@contextmanager
def transaction():
    try:
        current_app.logger.info("Transacting with database.")
        yield
        current_app.db.session.commit()
    except Exception as err:
        current_app.logger.info("An error occured in attempted transaction.")
        current_app.logger.error(err)
        current_app.db.session.rollback()
        raise err
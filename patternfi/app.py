import os
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=config.Config):

    """Construct the core application."""

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)
    app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = True
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db)    

    setattr(app, "db", db)

    with app.app_context():
        import routes
        return app

if __name__ == "__main__": 

    app = create_app()
    app.run(debug=True, port=5000)
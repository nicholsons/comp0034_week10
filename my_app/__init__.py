import os
from pathlib import Path
import pandas as pd
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
photos = UploadSet('photos', IMAGES)


def create_app(config_classname):
    """
    Initialise and configure the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)

    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #csrf.init_app(app)
    configure_uploads(app, photos)

    with app.app_context():
        from my_app.models import User, Profile, Area
        db.create_all()

        # Add the local authority data to the database (this is a workaround you don't need this for your coursework!)
        csv_file = Path(__file__).parent.parent.joinpath("data/household_recycling.csv")
        df = pd.read_csv(csv_file, usecols=['Code', 'Area'])
        df.drop_duplicates(inplace=True)
        df.set_index('Code', inplace=True)
        df.to_sql('area', db.engine, if_exists='replace')

        # Add sample data for the REST API exercise
        u = User.query.first()
        if u is None:
            p1 = Profile(username='jo_b', bio='something about me', area='Barnet')
            p2 = Profile(username='fred_s', bio='something interesting', area='Barnet')
            u1 = User(firstname='Jo', lastname='Bloggs', email='jo@bloggs.com', profiles=[p1])
            u2 = User(firstname='Fred', lastname='Smith', email='fred@smith.com', profiles=[p2])
            u3 = User(firstname='Santa', lastname='Claus', email='gift@northpole.org')
            u4 = User(firstname='Robert', lastname='Plant', email='raising_sand@blues.com')
            u1.set_password('test')
            u2.set_password('test')
            u3.set_password('test')
            u4.set_password('test')
            db.session.add_all([u1, u2, u3, u4])
            db.session.commit()

        from dash_app.dash import init_dashboard
        app = init_dashboard(app)

    from my_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from my_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app

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
    Initialises and configures the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    configure_uploads(app, photos)

    with app.app_context():
        from my_app.models import User, Country, Profile
        db.create_all()
        add_countries(app)

        from dash_app.dash import init_dashboard
        app = init_dashboard(app)

    from my_app.main.main import main_bp
    app.register_blueprint(main_bp)

    from my_app.auth.auth import auth_bp
    app.register_blueprint(auth_bp)

    from my_app.community.community import community_bp
    app.register_blueprint(community_bp)

    return app


def add_countries(app):
    """
    Adds the list of countries to the database if it doesn't already exist
    :param app:
    """
    from my_app.models import Country
    exists = Country.query.filter_by(id=1).scalar() is not None
    if not exists:
        data_path = app.config['DATA_PATH']
        with open(data_path.joinpath('countries.txt'), "r") as countries:
            for country in countries:
                country = country.split("|")
                country[1] = country[1].rstrip('\n')
                c = Country(country_name=country[1])
                db.session.add(c)
            db.session.commit()

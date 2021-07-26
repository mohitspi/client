from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from flask_mail import Mail, Message
from flask_migrate import Migrate #NEW

db = SQLAlchemy()

mail = Mail()
DB_NAME1 = "main.db"
# Added
DB_NAME2 = 'data.db'

BACKEND_URL = "http://127.0.0.1:8080/"
def create_app():
    app = Flask(__name__, static_url_path='')
    app.config['SECRET_KEY'] = "RandomString"

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME1}'
    app.config['SQLALCHEMY_BINDS'] ={
        'db2': f'sqlite:///{DB_NAME2}'
    }

    migrate = Migrate(app, db) #NEW
    db.init_app(app)
    migrate.init_app(app, db) #NEW

    from .viewables import viewables
    from .auth import auth
    from .sample import sample
    from .virtualManager import virtualManager
    from .cisco import cisco_new

    app.register_blueprint(viewables, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(virtualManager, url_prefix='/virtualManager')
    app.register_blueprint(sample, url_prefix='/response')
    app.register_blueprint(cisco_new, url_prefix='')

    from .models import User

    with app.app_context():
        db.create_all(app=app)
        db.create_all(bind=['db2'])

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

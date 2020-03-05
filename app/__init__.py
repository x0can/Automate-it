from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

# user_manager = UserManager

def create_app(config_name):
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False





   
    app.config.from_object(config_options[config_name])
    from .models import User

    

    db.init_app(app)
    
    from .main import main as main_blueprint
    

    app.register_blueprint(main_blueprint)
    with app.app_context():
        from .main import views
        db.create_all()


        return app


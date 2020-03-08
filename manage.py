import os
from app import create_app, db
from flask_script import Manager,Server
from app.models import *
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from app.main import views
from app import models,resources
from flask_jwt_extended import JWTManager
from config import Config





app = create_app("production")
manager = Manager(app)
manager.add_command("server",Server)
jwt = JWTManager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
api = Api(app)


app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    tok = decrypted_token['jti']
    return models.RevokeToken.is_tok_blacklisted(tok)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db, User=User,Detail=Detail)
    
@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    manager.run()
    
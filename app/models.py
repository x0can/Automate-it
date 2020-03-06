from . import db
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    pass_secure = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(100), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False    


class Detail(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.Integer,primary_key = True)
    model = db.Column(db.String(255))
    driver_name = db.Column(db.String(255))
    owner_name = db.Column(db.String(255))
    owner_email = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    eng_no = db.Column(db.String(255))
    reg_no = db.Column(db.String(255))
    mileage = db.Column(db.String(255))
    driver_no = db.Column(db.String(255))












        
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

        # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)






class Role (db.Model):
    __tablename__= 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.name}'


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))    


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












        
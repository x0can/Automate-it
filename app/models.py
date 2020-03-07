from . import db
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    pass_secure = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(100), nullable=False)

    def  hash_password(self, password):
        self.pass_secure=pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.pass_secure)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config_options['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token): 
        s = Serializer(app.config_options['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None

        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    @auth.verify_password
    def verify_password(email_or_token, password):

        user = User.verify_auth_token(email_or_token)
        if not user:
            user = User.query.filter_by(email=email_or_token).first()

            if not user or not user.verify_password(password):
                return False

        g.user = user
        return True





    


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












        
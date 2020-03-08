from . import db
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.hash import pbkdf2_sha256 as sha256


auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    pass_secure = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(20), nullable=False)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def generate_hash(pass_secure):
        return sha256.hash(pass_secure)

    @staticmethod
    def verify_hash(pass_secure, hash):
        return sha256.verify(pass_secure, hash) 


    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(j):
            return{
                'email':j.email,
                'role':j.roles,
                'username':j.username,
                'password':j.pass_secure
            }
        return {'users': list(map(lambda j: to_json(j), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}

        except:
            return {'message': 'Something went wrong'}                

   
class RevokeToken(db.Model):
    __tablename__='revoke_token'
    id=db.Column(db.Integer, primary_key=True)
    tok=db.Column(db.String(1000))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_tok_blacklisted(cls, tok):
        query = cls.query.filter_by(tok=tok).first()
        return bool(query)    
    


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
    


    @classmethod
    def return_all(cls):
        def to_json(j):
            return{
                'model':j.model,
                'driver_name':j.driver_name,
                'owner_name':j.owner_name,
                'owner_email':j.owner_email,
                'company_name':company_name,
                'eng_no':eng_no,
                'reg_no':reg_no,
                'mileage':mileage,
                'driver_no':driver_no

            }
        return {'Detail': list(map(lambda j: to_json(j), Detail.query.all()))}


    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}

        except:
            return {'message': 'Something went wrong'}






        
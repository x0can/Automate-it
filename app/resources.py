from flask_restful import Resource, reqparse
from app.models import User as UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app.models import RevokeToken,Detail
from flask import Flask, jsonify, render_template, redirect, url_for,request



parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('username', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank', required = False)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return{'message': 'User {} already exists'. format(data['email'])}

        new_user = UserModel(
            username = data['username'],
            pass_secure = UserModel.generate_hash(data['password']),
            email = data['email'],
            roles=data['role']
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])

            return {
                'message': 'User {} was created'.format( data['username']),
                'access_token': access_token,
                'refresh_token':refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_email(data['email'])
        if not current_user:
            return {'message': 'User {} with email: {} doesn\t exist'.format(data['username'], data['email'])}

        if  UserModel.verify_hash(data['password'], current_user.pass_secure):
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])


            return {
                'status' : 'success',
                'message': 'Logged in as {}'.format(current_user.username),
                'role': '{}'.format(current_user.roles),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return{
                'status': 'failed',
                'message': 'Wrong credentials'
            }    

        return data
      
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        tok = get_raw_jwt()['jti']
        try:
            revoked_token = RevokeToken(tok=tok)
            revoked_token.add()
            return {
                'status': 'logout',
                'message':'Access token has been revoked'
                }

        except:
            return {'message': 'Something went wrong'},500    
        # return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        tok = get_raw_jwt()['jti']
        try:
            revoked_token = RevokeToken(tok=tok)
            revoked_token.add()
            return {
                'status':'logout',
                'message': 'Refresh token has been revoked'
                }
        except:
            return {'message': 'Something went wrong'}, 500

      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user=get_jwt_identity()
        access_token=create_access_token(identity=current_user)
        return{
            'access_token': access_token
        }
        return {'message': 'Token refresh'}
      
      
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()

class AllVehicles(Resource):
    def get(self):
        return Detail.return_all()

    def delete(self):
        return Detail.delete_all()

class NewVehicle(Resource):
    def post(self):
        pass

      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        # details = Detail
        # p = parser.add_argument('email', help='This is required to access detais')

        # data = parser.parse_args()
        # user = UserModel.find_by_email(email=data['email'])

        # print(user)
        # if user.roles=="attendant":
        #     return {'message': 'attendant found'}
        # if user.roles=="mechanic":
        #     return {'message': 'mechanic found'}
        # return {'message': 'Account no valid'}        
            
        return {
            'answer': 89
        }

# class AllDetail(Resource):
#     @jwt_required
#     def post(self):
        
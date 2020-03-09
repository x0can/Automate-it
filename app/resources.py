from flask_restful import Resource, reqparse
from app.models import User as UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app.models import *
from flask import Flask, jsonify, render_template, redirect, url_for,request



parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('username', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank', required = False)


detail = reqparse.RequestParser()
detail.add_argument('model',help = 'This field cannot be blank', required = True)
detail.add_argument('driver_name',help = 'This field cannot be blank', required = True)
detail.add_argument('owner_name',help = 'This field cannot be blank', required = True)
detail.add_argument('owner_email',help = 'This field cannot be blank', required = True)
detail.add_argument('company_name',help = 'This field cannot be blank', required = True)
detail.add_argument('engine',help = 'This field cannot be blank', required = True)
detail.add_argument('reg_no',help = 'This field cannot be blank', required = True)
detail.add_argument('mileage',help = 'This field cannot be blank', required = True)
detail.add_argument('driver_no',help = 'This field cannot be blank', required = True)


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


class NewCustomer(Resource):
    @jwt_refresh_token_required    
    def post(self):
        data = detail.parse_args()
        user = parser.parse_args()
        current_user= UserModel.find_by_email(user['email'])
        current_vehicle = Vehicle.find_by_reg_no(data['reg_no'],data['engine'])
        current_customer = Customer.find_by_email(data['owner_email'])
        # print(current_customer.id)
       
        try:            
            if not current_user:
                return {
                    'status': 'failed',
                    'message': 'User {} with email: {} is not permitted'.format(user['username'], user['email']),
                }
            if not current_user.roles=="attendant":
                return {
                    'status':'failed',
                    'message': 'User {} with email: {} is not allowed'.format(user['username'], user['email']),
                    }
            
                        
            if current_vehicle:
                return {
                    'status': 'failed',
                    'message': 'Vehicle {} with regestration {} already exists'.format(data['model'],data['reg_no'])
                }

            if current_customer:
                customer_id = current_customer.id
                new_vehicle = Vehicle(
                    model=data['model'],
                    reg_no=data['reg_no'],
                    mileage=data['mileage'],
                    eng_no=data['engine'],
                    customer_id=customer_id
                    )

                try:
                    new_vehicle.save_to_db()
                    return{
                            'status':'new vehicle added',
                            'model':new_vehicle.model,
                            'reg_no':new_vehicle.reg_no,
                            'mileage':new_vehicle.mileage,
                            'eng_no':new_vehicle.eng_no,
                        }
                except:
                    return{
                        'status':'failed',
                        'message':'something went wrong'
                    },500
            else:
                
                new_customer = Customer(
                    driver_name=data['driver_name'],
                    driver_no=data['driver_no'],
                    owner_name=data['owner_name'],
                    owner_email=data['owner_email'],
                    company_name=data['company_name'],

                    )
                new_customer.save_to_db()
                print(new_customer.id)
                try:
                    customer_id=new_customer.id
                    new_vehicle = Vehicle(
                            model=data['model'],
                            reg_no=data['reg_no'],
                            mileage=data['mileage'],
                            eng_no=data['engine'],
                            customer_id=customer_id
                        )
                    print(new_vehicle.model)
                    new_vehicle.save_to_db()
                    return{
                            'status':'new customer added',
                            'driver_name':new_customer.driver_name,
                            'owner_email':new_customer.owner_email
                        }
                
                except:
                    return {'message': 'Something went wrong'}, 500
        except:
            return {'message': 'Something went wrong'},500    
            

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

# class AllVehicles(Resource):
#     def get(self):
#         return Detail.return_all()

#     def delete(self):
#         return Detail.delete_all()

# class NewVehicle(Resource):
#     def post(self):
#         pass

      
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
        
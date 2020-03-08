import requests,json
from flask import Flask, jsonify, render_template, redirect, url_for,request
from .import main
from app.models import Detail,User
from ..import db
import app
import datetime
from functools import wraps
from werkzeug.exceptions import abort
import jwt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app.models import RevokeToken,Detail


newCustomer=[];
        
@main.route("/", methods=["GET"])
def index():
    return redirect('/welcome')

@main.route("/get_user", methods=["GET", "POST"])
def get_role():
   
    result = request.form.to_dict(flat=False)
    result = {
                    key: value[0] if len(value)== 10 else value
                    for key, value in request.form.items()
                }
                
    print(result)
    try:
        current_user = User.find_by_email(result['email'])
        if not current_user:
            message = 'User {} with email: {} doesn\t exist'.format(result['username'], result['email'])
            return render_template('login.html',message=message)

        if User.verify_hash(result['password'],current_user.pass_secure):
            
            access_token = create_access_token(identity=result['email'])
            refresh_token = create_refresh_token(identity=result['email'])

            if current_user.roles=="attendant":
                email=current_user.email
                password=result['password']
                message="Welcome {}".format(current_user.username)
                return render_template('index.html',message=message, password=password,email=email)

            message="Welcome {}".format(current_user.username)    
            return render_template('mechanic.html',message=message)    
        else:
            message="Please check password"
            return render_template('login.html',message=message)
    except:
        return render_template("authorize.html")



@main.route("/register", methods=["GET","POST"])
def register_user():    
    
    result = request.form.to_dict(flat=False)
    result = {
                    key: value[0] if len(value)== 10 else value
                    for key, value in request.form.items()
                }
    print(result)
    try:
        if User.find_by_email(result['email']):
            message='user {} already exists'.format(result['email'])
            return render_template("register.html", message=message)
        new_user = User(
            username = result['username'],
            pass_secure = User.generate_hash(result['password']),
            email = result['email'],
            roles=result['roles']
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=result['email'])
            refresh_token = create_refresh_token(identity=result['email'])

            if result['roles']=='attendant':
                return redirect("index.html")
            elif result['roles']!="attendant" and result['roles'] != "mechanic":
                return render_template("fourOwfour.html")
            else:
                return render_template("mechanic.html")       
        except:
            pass
    except:
        pass

    return render_template("register.html")
    

@main.route('/error_registration', methods=['GET','POST'])
def error_regestration():
    message="email already exists"    
    pass
@main.route("/welcome",methods=["GET", "POST"])
def login_user():
    return render_template("login.html") 


@main.route("/post_field", methods=["GET", "POST"])
def need_input():

    try:
        result = request.form.to_dict(flat=False)
        result = {
            key: value[0] if len(value)== 10 else value
            for key, value in request.form.items()
        }
        newCustomer.append(result)

        if result['owner']=="":
            result['owner']==result['driverName']

            details = Detail(model=result["model"], driver_name=result["driverName"],
            owner_name=result["owner"],owner_email=result["email"],company_name= result["company"],
            eng_no =result["engNo"], reg_no=result["regNo"], mileage=result["mileage"],driver_no=result["driverNo"]
            )
            db.session.add(details)
            db.session.commit()
            data = details.query.filter_by(id=details.id).first()
            print(data)
        else:
            details = Detail(model=result["model"], driver_name=result["driverName"],
            owner_name=result["owner"],owner_email=result["email"],company_name= result["company"],
            eng_no =result["engNo"], reg_no=result["regNo"], mileage=result["mileage"],driver_no=result["driverNo"]
            )
            db.session.add(details)
            db.session.commit()
            data = details.query.filter_by(id=details.id).first()

        if result["owner"]=="":
            owner = result["driverName"]    
            drivername= result['driverName']
            email = result["email"]
            mileage = mileage=result["mileage"]
            company = result["company"]    
        else:
            owner = result["owner"]
            drivername= result['driverName']
            email = result["email"]
            mileage = mileage=result["mileage"]
            company = result["company"]        
        context = {
                "owner":owner,
                "driver":drivername,
                "email":email,
                "mileage":mileage,
                "company":company,
            }
        return render_template('thanks.html',data = data, result=result,context=context)
    except KeyError or AttributeError:
        return render_template("fourOwfour.html")





@main.route("/attendant", methods=["GET","POST"])
@jwt_refresh_token_required
def driver_information():
    current_user =get_jwt_identity()
    print(current_user)
    access_token=create_access_token(identity=current_user)
    # message = "Hello {}".format(email)
    # return render_template("index.html")
    return{
            'access_token': access_token
        }
    return {'message': 'Token refresh'}

@main.route("/mechanic", methods=["GET","POST"])
def make_vehicle():

    while len(newCustomer)>0:
        message="You are needed, there is a new customer"
        model=Detail.query.filter_by(mod=Detail.model).first()
        plate=Detail.query.filter_by(pla=Detail.reg_no).first()
        otherVehicles=Detail.query.all()[1::10]
        allVehicles=Detail.query.filter_by(mod=Detail.model).all()
        
        context={
                "message":message,
                "model":model,
                "plate":plate,
                "otherVehicles":otherVehicles,
                "allVehicles":allVehicles,
            }
        return render_template("mechanic.html")
        break

    return render_template("mechanic.html")    

    
   


        
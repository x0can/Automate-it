# import requests,json
from flask import Flask, jsonify, render_template, redirect, url_for,request
from .import main
from app.models import Detail,User
from ..import db
import datetime
# from flask_login import login_required
# from flask import LoginManager

# from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from functools import wraps
from werkzeug.exceptions import abort
import jwt



# auth = HTTPBasicAuth()
newCustomer=[];

# def restricted(access_level):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             access_level.get_role.session

#             return func(*args, **kwargs)
#         return wrapper
#     return decorator        
    
@main.route("/", methods=["GET"])
def index():
    return redirect('/login')

@main.route("/get_user", methods=["GET", "POST"])
def get_role():

    
    result_user = request.form.to_dict(flat=False)
    result_user = {
            key: value[0] if len(value)== 1 else value
            for key, value in request.form.items()
        }
    

    email = result_user["email"]
    password = result_user["password"]
    username = result_user["username"]
    user = User.query.filter_by(email=email).first()
    print(user)
    try:

        if user.email != email:
            message = "Invalid credentials"
            # print(message)
            return redirect("/login", message)
        if user.roles=="attendant":
            return redirect("/attendant")
        if user.roles=="mechanic":
            return redirect("/mechanic")
        else:
            message="You must be regestered this account is invalid"
            return render_template("login.html", message=message)
    except AttributeError:
            message="You must be regestered this account is invalid"
            return render_template("login.html",message=message)
                
    
    # if result_user["email"]=="":
    #     return render_template("access.html")
    # else:        
    #     if user.email==result_user["email"]:
    #         if user.roles=="attendant":
    #             return redirect("/attendant")
    #         if user.roles=="mechanic":
    #             return redirect("/mechanic")
    #         else:
    #             return render_template("fourOwfour.html")            
    #     else:
    #         message="Invalid credentials"
    #         return render_template("register.html",message=message)

    # print(result_user)
    # if result_user["roles"]=="attendant":
    #     return redirect('/attendant')            
    # else:
    #     return redirect('/mechanic')


@main.route("/register", methods=["GET","POST"])
def register_user():

    try:
        result = request.form.to_dict(flat=False)
        result = {
                key: value[0] if len(value)== 10 else value
                for key, value in request.form.items()
            }

        if result["username"] is None or result["email"] is None or result["password"] is None or result["confirmPassword"]!=result["password"]:
            message = "missing fields, please fill all the fields"
            
            return render_template("register.html",message=message)    
       
        if User.query.filter_by(email=result["email"]).first() is not None:
            message="email already exists"
            return render_template("register.html",message=message)
        else:
            user=User(username=result["username"],email=result["email"],pass_secure=result["password"],roles=result["roles"])
            user.hash_password(result["password"])
            db.session.add(user)
            db.session.commit()

            if user.roles=="attendant":
                return redirect("/attendant")
            if user.roles=="mechanic": 
                return redirect("/mechanic")
            
        return render_template("register.html")

    
    except KeyError or AttributeError:
        message="Account not valid"
        return render_template("register.html")

    else:
        return render_template("register.html")
   


@main.route("/login",methods=["GET", "POST"])
def login_user():
# def encode_auth_token(self,user_id):
    user_id=User.query.filter_by(id=User.id)
    try:
        payload = {
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat':datetime.datetime.utcnow(),
            'sub':user_id
            }
        body = jwt.encode(
            payload,
            main.config.get('SECRET_KEY'),
                algorithm="HOUSE788CARDS"
            )
        print(body)
        return body

    except Exception as e:
        print(e)    
    
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
# @login_required
def driver_information():
    return render_template("index.html")

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
        return redirect('/mechanic', message)
        break

    return render_template("mechanic.html")    

    
   


        
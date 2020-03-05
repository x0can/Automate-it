# import requests,json
from flask import Flask, jsonify, render_template, redirect, url_for,request
from .import main
from app.models import Detail,User,Role
from ..import db
import datetime
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin


@main.route("/post_field", methods=["GET", "POST"])
def need_input():

    try:
        result = request.form.to_dict(flat=False)
        result = {
            key: value[0] if len(value)== 1 else value
            for key, value in request.form.items()
        }

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
        
    except KeyError:
        return render_template("fourOwfour.html")
    






@main.route("/", methods=["GET"])
def get_form():
  
    return render_template('index.html')

# @main.route('/',methods=['GET'])
# def create_user():
#     username = request.args.get('user')
#     email = redirect.args.get('email')
#     if username and email:
#         new_user = User(username=username,email=email,role=)    
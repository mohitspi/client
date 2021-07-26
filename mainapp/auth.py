from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from .models import User
from .import db
from flask_login import login_user,login_required,logout_user,current_user
from . import BACKEND_URL
import base64,datetime
import requests,json
auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
   if current_user and current_user.is_authenticated:
      return redirect(url_for('viewables.home'))
   return render_template('auth/auth.html')

@auth.route('/logout')
@login_required
def logout():
   user = User.query.filter_by(id=current_user.id).first()
   db.session.delete(user)
   db.session.commit()
   logout_user()

   return redirect(url_for('auth.login'))

@auth.route('/login',methods=['POST'])
def authBySkeyAndApiToken():
   mysecret = request.form.get('mysecret')
   apitoken = request.form.get('apitoken')
   payload = {
      'res' : 'SUCCESS',
      'mysecret': mysecret,
      'apitoken' : apitoken
   }
   sendRes = requests.post(BACKEND_URL+'auth/api/authenticate/user', data=json.dumps(payload))
   print("getRes", getRes)

   getRes = sendRes.json()

   print("getRes", getRes)
   
   try:
      email = getRes['email']
      exist = User.query.filter_by(email=email)
   except :
      exist = None

   print("exist",exist)
      
   if exist:
        [db.session.delete(x) for x in exist]
        db.session.commit()

   if getRes['res'] == "SUCCESS":
      email = getRes['email']
      mysecret = getRes['mysecret']
      apitoken = getRes['apitoken']
      simplepass = getRes['simplepass']
      new_auth = User(email=email,mysecret=mysecret,apitoken=apitoken,simplepass=simplepass)
      db.session.add(new_auth)
      db.session.commit()
      login_user(new_auth,remember=True)
      return redirect(url_for('viewables.home'))
   else:
      return redirect(url_for('sample.response_basic_view',err_body="Wrong Credentials"))

      new_auth = User(email='mohir@gmail.com',mysecret='mysecret',apitoken='apitoken',simplepass='simplepass')



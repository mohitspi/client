import os,sys
sys.path.append(os.path.abspath(os.path.join('..','mainapp')))

from mainapp.models import User, Two_factor_code, EmailConfirmCode, PhoneConfirmCode
import re, random, datetime

from mainapp import db

from mainapp.utility.twilio_otp import getOTPApi


def __sign_up_validation(name, email, password1, password2, phone):
    if name == "" or len(name.replace(" ", "")) == 0:
        return 'Full name is empty'
    if password1 != password2:
        return 'Password and Confirm Password is not same'
    if len(password1) < 8:
        return 'Password is too small'

    # You can use regex for more supper strong password
    # Here is the regex 

    REGEX = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[{}:;/><+=()#?!@$%^&*-]).{8,}$'
    StrongPass = re.fullmatch(REGEX, password1)
    if not StrongPass:
        return 'Weak password add one capital, one small ,one special character and a digit in password'

    # Not mandatory but if u ever want to use that , u can do that :) with this regex code easily . 

    user = User.query.filter_by(email=email).first()
    if user:
        return 'Email already exists'
    user = User.query.filter_by(phone=phone).first()
    if user:
        return 'Phone already exists'
    return ""


def __emailConfirmCode(user):
    exist = EmailConfirmCode.query.filter_by(user_id=user.id)
    if exist:
        [db.session.delete(x) for x in exist]
        db.session.commit()
        otp = str(random.randint(100000, 999999))
        exp = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
        user_id = user.id
    else:
        otp = str(random.randint(100000, 999999))
        exp = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
        user_id = user.id
    return True, otp, exp, user_id


def __phoneConfirmCode(user):
    exist = PhoneConfirmCode.query.filter_by(user_id=user.id)
    if exist:
        [db.session.delete(x) for x in exist]
        db.session.commit()
        otp = str(random.randint(100000, 999999))
        exp = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
        user_id = user.id
        getOTPApi(user.phone, otp)
    else:
        otp = str(random.randint(100000, 999999))
        exp = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
        user_id = user.id
        getOTPApi(user.phone, otp)
    return True, otp, exp, user_id


def __generate_otp(user):
    exist = Two_factor_code.query.filter_by(user_id=user.id)
    if exist:
        [db.session.delete(x) for x in exist]
        db.session.commit()
        otp = str(random.randint(100000, 999999))
        exp = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
        user_id = user.id
        getOTPApi(user.phone, otp)
    else:
        otp = str(random.randint(100000, 999999))
        exp = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
        user_id = user.id
        getOTPApi(user.phone, otp)
    return True, user_id, otp, exp

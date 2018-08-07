from flask import Flask, render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL

import re
email_veri = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_check= re.compile(r'^[a-zA-Z]+$')
password_check= re.compile(r'\d.+[A-Z]|[A-Z].+\d')

app= Flask(__name__)
bcrypt = Bcrypt(app) 

app.secret_key="DANKMEMESARENEVERDANKENOUGH"

@app.route('/')
def home():
    return render_template("home.html", **session)

@app.route('/register', methods=["post"])
def register():
    valid = True
    
    mysql = connectToMySQL('LoginAndRegistration')
    query = "SELECT * from users WHERE email = %(email)s"
    data = {"email" : request.form['email']}
    row = mysql.query_db(query, data)

    if len(row) > 0:
        flash("An account already has registered with the same email")
        valid = False
    elif len(request.form['email']) <1 :
        flash("Email cannot be blank")
        print("thisisworking")
        valid = False
    elif not email_veri.match(request.form['email']):
        flash("Invalid Email Address")
        valid = False

    if len(request.form['first_name']) < 1:
        flash("First name cannot be blank!")
        valid = False
    elif not name_check.match(request.form['first_name']):
        flash("First name can not contain numbers")
        valid = False
    
    if len(request.form['last_name']) < 1:
        flash("Last name cannot be blank!")
        valid = False
    elif not name_check.match(request.form['last_name']):
        flash("Last name can not contain numbers")
        valid = False
    
    if len(request.form['password']) < 1:
        flash("Password cannot be blank!")
        valid = False
    elif len(request.form['password'])<=8:
        flash("Password has to be at least 8 characters long")
    elif not request.form['password']==request.form['confirmpassword']:
        flash("Password does not match with the confirmation")
        valid=False
    elif not password_check.match(request.form['password']):
        flash("Password needs at least 1 uppercase and one 1numeric value")
        valid = False

    session['first_name']=request.form["first_name"]
    session['last_name']=request.form["last_name"]
    session['email']=request.form["email"]
    session['city']=request.form["city"]
    
    if not valid:
        return redirect('/')

    else:
        flash("Register Successful")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])  
    print(pw_hash)  
    
    mysql = connectToMySQL('LoginAndRegistration')

    query = "INSERT INTO users (first_name, last_name, email, password, birthday, city, state, gender, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, %(birthday)s, %(city)s, %(state)s, %(gender)s, now(), now());"
    
    request.form['password_hash'] = pw_hash
    stuff_id = mysql.query_db(query, request.form)
    
    return redirect("/")

@app.route('/login', methods=["post"])
def login():
    valid = True

    mysql = connectToMySQL('LoginAndRegistration')
    query = "SELECT * from users WHERE email = %(email)s"
    results = mysql.query_db(query, request.form)

    if results:
        print("DATABASE PASSWORD", hashfromdata)
    else:
        flash("Invalid Email")
        valid = False

    if len(request.form['email']) <1 :
        flash("Email cannot be blank")
        print("thisisworking")
        valid = False

    if len(request.form['password']) < 1:
        flash("Password cannot be blank!")
        valid = False
    
    if valid == False:
        return redirect ('/')
    
    if bcrypt.check_password_hash(hashfromdata, request.form['password']):
        session['userid'] = result[0]['id']
        return redirect("/success")
    
    else: 
        flash("Log in failed")
        return redirect ('/')

@app.route("/success")
def endpage():
     

    mysql = connectToMySQL('LoginAndRegistration')
    query = "SELECT first_name from users WHERE id = %(userid)s"
    user_firstname = mysql.query_db(query, session)

    print(user_firstname)

    return render_template("end.html", name=user_firstname[0]["first_name"])


if __name__=="__main__":
    app.run(debug=True)
"""Routes to the user auth page"""
import json
from flask import Blueprint, redirect, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    """user auth"""
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST' : #login and go to home page
        email = request.form['email']
        password = request.form['password']
        #storing users in a json file for now, very bad practice but fine for proof of concept
        with open('./website/users.json', 'r', encoding='utf-8') as json_file:
            users = json.load(json_file)
            for user in users:
                if user['email'] == email and user['password'] == password:
                    return render_template('index.html')
            #if not found, add user to json file
            users.append({'email': email, 'password': password}) 
            with open('./website/users.json', 'w', encoding='utf-8') as outfile:
                json.dump(users, outfile)

        return redirect('/app')

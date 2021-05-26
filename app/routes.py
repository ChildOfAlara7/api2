from flask import request, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, database
from app.database import get_db, init_db
from app.models import User
import re

@app.errorhandler(404)

@app.route('/')
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    bas = init_db()
    base = get_db()
    all = base.execute("SELECT * FROM users")
    return jsonify({'user':[dict(row) for row in all]})
 

@app.route('/show', methods=['GET', 'POST'])
@login_required
def show():
    id = int(request.args['id'])
    sr = User.query.filter_by(id=id).first()
    if sr is None:
        return 'id not registered', 404    
    if sr is None: 
        return 'missing id'
    res = {"id": sr.id,
            "login":sr.login,
            "password": sr.password_hash,
            "name": sr.name,
            "mail": sr.mail}
    return jsonify(res)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    id = int(request.args['id'])
    user = User.query.filter_by(id=id).first()
    if user is None:
        return 'id not registered', 404
    db.session.delete(user)
    db.session.commit()

    res = User.query.all()
    lis = []
    for sr in res:
        lis.append({"id": sr.id,
            "login":sr.login,
            "password": sr.password_hash,
            "name": sr.name,
            "mail": sr.mail}) 
    return jsonify(lis)  
            

@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.args['login']
    password = request.args['password']
    
    if current_user.is_authenticated:
        return 'already logged in'
    user = User.query.filter_by(login=login).first()
    if user is None or not user.check_password(password):
        return 'invalid data'
    login_user(user)
    return 'logged in'

@app.route('/logout')
def logout():
    logout_user()
    return 'logged out'

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return 'already registered'

    login = request.args['login']
    password = request.args['password']
    name = request.args['name']
    mail = request.args['mail']

    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail) is None:
        return 'invalid input', 404
    if re.match("[a-zA-Z]+", name) is None:
        return 'invalid input', 404

    user_name = User.query.filter_by(login=login).first()
    if user_name is not None:
        return 'login is already registered', 404

    user_mail = User.query.filter_by(mail=mail).first()
    if user_mail is not None:
        return 'mail is already registered', 404

    user = User(login=login, mail=mail, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return 'registered'


@app.route('/showall')
@login_required
def all():
    res = User.query.all()
    lis = []
    for sr in res:
        lis.append({"id": sr.id,
            "login":sr.login,
            "password": sr.password_hash,
            "name": sr.name,
            "mail": sr.mail})    
    return jsonify(lis)

from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app import app
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/create_user', methods = ['post'])
def create_user():
    print(request.form)
    if not User.user_validator(request.form):
        return redirect('/')
    if User.get_user_by_email(request.form):
        flash('email is already in use or your password and confirm password do not match')
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    print(data['password'])
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login', methods = ['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash('Email/ Password is invalid')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Email/ Password is invalid')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/success')

@app.route('/success')
def success():
    if 'user_id' not in session:
        flash('Please login before accesing this page')
        return redirect('/')
    return render_template('dashboard.html',user = User.get_user_by_id(session['user_id']),all_workouts = User.get_users_with_workouts())

@app.route('/dashboard')
def go_to_dashbaord():
    return redirect('/success')

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')

@app.route('/account/<int:id>')
def show_account_page(id):
    data = {
        'id': id
    }
    return render_template("account.html", one_user = User.get_one_user(data))

@app.route('/edit_user/<int:id>', methods = ['post'])
def edit_user(id):
    print(request.form)
    if not User.user_update_validator(request.form):
        return redirect(f'/account/{id}')
    User.update_user(request.form, id)
    return redirect('/success')
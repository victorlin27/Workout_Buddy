from flask import render_template, redirect, request, session, flash
from flask_app.models.workout_model import Workout
from flask_app import app

@app.route('/add_workout')
def show_add_page():
    if 'user_id' not in session:
        flash('Please login before accesing this page')
        return redirect('/login')
    return render_template('add_workout.html')

@app.route('/create_workout', methods =['post'] )
def create_magazine():
    if not Workout.workout_validator(request.form):
        return redirect('/add_workout')
    data = {
        'workout_name': request.form['workout_name'],
        'description': request.form['description'],
        'id' : session['user_id']
    }
    Workout.save_workout(data)
    return redirect('/success')

@app.route('/show_workout/<int:id>')
def show_one_magazine(id):
    data = {
        'id' : id
    }
    return render_template('show_workout.html',one_workout = Workout.get_one_workout(data))

@app.route('/delete/<int:id>')
def delete_user(id):
    Workout.delete_workout(id)
    return redirect('/success')

@app.route('/show_workout_edit/<int:id>')
def show_workout_page(id):
    data = {
        'id' : id
    }
    return render_template('edit_workout.html', one_workout = Workout.get_one_workout(data))

@app.route('/edit_workout/<int:id>', methods = ['post'])
def update_workout(id):
    print (request.form)
    Workout.update_workout(request.form, id)
    return redirect('/success')
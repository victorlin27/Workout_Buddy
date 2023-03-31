from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model

db = 'workout_buddy'

class Workout :
    def __init__(self,data):
        self.id = data['id']
        self.workout_name = data['workout_name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save_workout(cls,data):
        query = "INSERT INTO workouts (workout_name,description, user_id) VALUES (%(workout_name)s,%(description)s, %(id)s )"
        return connectToMySQL(db).query_db(query,data)
    

    @classmethod
    def get_one_workout(cls, data):
        query = "SELECT * FROM workouts JOIN users ON workouts.user_id = users.id  where workouts.id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        workout = cls(results[0])
        user_dictionary = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
        }
        workout.user = user_model.User(user_dictionary)
        return workout
    
    @classmethod
    def delete_workout(cls,id):
        query = f"DELETE FROM workouts where id = {id}"
        return connectToMySQL(db).query_db(query)
    
    @classmethod
    def update_workout(cls,data,id):
        query = f'''
        UPDATE workouts
        set workout_name = %(workout_name)s, description = %(description)s
        WHERE id = {id}
        '''
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def workout_validator(workout):
        is_valid = True

        if len(workout['workout_name']) < 2:
            flash('Your workout name needs to be at least 2 characters long')
            is_valid = False

        if len(workout['description']) < 10:
            flash('Your decription needs to be at least 10 characters long')
            is_valid = False
        return is_valid
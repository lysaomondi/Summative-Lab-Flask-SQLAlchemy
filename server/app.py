from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from config import Config

from models import (
    db,
    Exercise,
    Workout,
    WorkoutExercise
)

from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():

    return {
        "message": "Welcome to Workout Tracker API"
    }, 200


@app.route("/workouts", methods=["GET"])
def get_workouts():

    workouts = Workout.query.all()

    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):

    workout = Workout.query.get_or_404(id)

    return workout_schema.dump(workout), 200


@app.route("/workouts", methods=["POST"])
def create_workout():

    try:

        data = workout_schema.load(request.json)

        workout = Workout(**data)

        db.session.add(workout)
        db.session.commit()

        return workout_schema.dump(workout), 201

    except ValidationError as error:

        return {"errors": error.messages}, 400

    except Exception as error:

        db.session.rollback()

        return {"error": str(error)}, 400


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):

    workout = Workout.query.get_or_404(id)

    db.session.delete(workout)
    db.session.commit()

    return {}, 204


@app.route("/exercises", methods=["GET"])
def get_exercises():

    exercises = Exercise.query.all()

    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):

    exercise = Exercise.query.get_or_404(id)

    return exercise_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():

    try:

        data = exercise_schema.load(request.json)

        exercise = Exercise(**data)

        db.session.add(exercise)
        db.session.commit()

        return exercise_schema.dump(exercise), 201

    except ValidationError as error:

        return {"errors": error.messages}, 400

    except Exception as error:

        db.session.rollback()

        return {"error": str(error)}, 400


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):

    exercise = Exercise.query.get_or_404(id)

    db.session.delete(exercise)
    db.session.commit()

    return {}, 204


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def create_workout_exercise(workout_id, exercise_id):

    workout = Workout.query.get_or_404(workout_id)

    exercise = Exercise.query.get_or_404(exercise_id)

    try:

        data = workout_exercise_schema.load(request.json)

        workout_exercise = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            reps=data["reps"],
            sets=data["sets"],
            duration_seconds=data["duration_seconds"]
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return workout_exercise_schema.dump(workout_exercise), 201

    except ValidationError as error:

        return {"errors": error.messages}, 400

    except Exception as error:

        db.session.rollback()

        return {"error": str(error)}, 400


if __name__ == "__main__":

    app.run(
        port=5555,
        debug=True
    )
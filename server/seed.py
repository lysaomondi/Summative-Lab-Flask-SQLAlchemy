from datetime import date

from app import app
from models import (
    db,
    Exercise,
    Workout,
    WorkoutExercise
)


with app.app_context():

    print("Deleting old data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()


    print("Creating exercises...")


    pushups = Exercise(
        name="Push Ups",
        category="Strength",
        equipment_needed=False
    )


    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )


    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )


    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )


    db.session.add_all([
        pushups,
        squats,
        running,
        plank
    ])


    db.session.commit()



    print("Creating workouts...")


    workout1 = Workout(
        date=date.today(),
        duration_minutes=45,
        notes="Morning strength workout"
    )


    workout2 = Workout(
        date=date.today(),
        duration_minutes=30,
        notes="Evening cardio workout"
    )


    db.session.add_all([
        workout1,
        workout2
    ])


    db.session.commit()



    print("Creating workout exercises...")


    workout_exercises = [

        WorkoutExercise(
            workout=workout1,
            exercise=pushups,
            reps=15,
            sets=3,
            duration_seconds=0
        ),


        WorkoutExercise(
            workout=workout1,
            exercise=squats,
            reps=20,
            sets=4,
            duration_seconds=0
        ),


        WorkoutExercise(
            workout=workout2,
            exercise=running,
            reps=0,
            sets=1,
            duration_seconds=1200
        ),


        WorkoutExercise(
            workout=workout2,
            exercise=plank,
            reps=0,
            sets=3,
            duration_seconds=60
        )

    ]


    db.session.add_all(
        workout_exercises
    )


    db.session.commit()


    print("Done!")
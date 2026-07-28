from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    reps = db.Column(
        db.Integer,
        nullable=False
    )

    sets = db.Column(
        db.Integer,
        nullable=False
    )

    duration_seconds = db.Column(
        db.Integer,
        nullable=False
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    @validates("sets")
    def validate_sets(self, key, value):
        if value <= 0:
            raise ValueError("Sets must be greater than zero.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value < 0:
            raise ValueError("Reps cannot be negative.")
        return value

    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if value < 0:
            raise ValueError("Duration cannot be negative.")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(
        db.Date,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be greater than zero.")
        return value


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    category = db.Column(
        db.String,
        nullable=False
    )

    equipment_needed = db.Column(
        db.Boolean,
        nullable=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("category")
    def validate_category(self, key, value):
        allowed = [
            "Strength",
            "Cardio",
            "Flexibility",
            "Balance",
            "Core"
        ]

        if value not in allowed:
            raise ValueError(f"Category must be one of {allowed}")

        return value
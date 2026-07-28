from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError,
    validate
)


class ExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=3,
            error="Exercise name must be at least 3 characters."
        )
    )

    category = fields.Str(required=True)

    equipment_needed = fields.Bool(required=True)

    workouts = fields.Nested(
        "WorkoutSchema",
        many=True,
        only=("id", "date", "duration_minutes"),
        dump_only=True
    )

    @validates("category")
    def validate_category(self, value, **kwargs):

        allowed = [
            "Strength",
            "Cardio",
            "Flexibility",
            "Balance",
            "Core"
        ]

        if value not in allowed:
            raise ValidationError(
                f"Category must be one of {allowed}"
            )


class WorkoutExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)

    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(required=True)

    sets = fields.Int(required=True)

    duration_seconds = fields.Int(required=True)

    @validates("sets")
    def validate_sets(self, value, **kwargs):

        if value <= 0:
            raise ValidationError(
                "Sets must be greater than zero."
            )

    @validates("reps")
    def validate_reps(self, value, **kwargs):

        if value < 0:
            raise ValidationError(
                "Reps cannot be negative."
            )

    @validates("duration_seconds")
    def validate_duration_seconds(self, value, **kwargs):

        if value < 0:
            raise ValidationError(
                "Duration cannot be negative."
            )


class WorkoutSchema(Schema):

    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(required=True)

    notes = fields.Str(allow_none=True)

    exercises = fields.Nested(
        ExerciseSchema,
        many=True,
        only=(
            "id",
            "name",
            "category",
            "equipment_needed"
        ),
        dump_only=True
    )

    @validates("duration_minutes")
    def validate_duration_minutes(self, value, **kwargs):

        if value <= 0:
            raise ValidationError(
                "Workout duration must be greater than zero."
            )


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
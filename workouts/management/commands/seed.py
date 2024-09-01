from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from workouts.models import Interval, Workout
from workouts.models.duration import (
    TimeDuration,
    DistanceDuration,
    PowerDuration,
    BaseDuration,
)
from workouts.models.utils import (
    create_warmup,
    create_cool_down,
    create_interval,
    create_repeat,
    build_workout,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with sample workout data."

    def handle(self, *args, **kwargs):
        self.seed_workouts()

    def seed_workouts(self):
        author = (
            User.objects.first()
        )  # Replace with a specific user or adjust as needed

        # Create the first workout
        warmup1 = create_warmup(
            duration_value=10,
            duration_type=BaseDuration.DurationType.TIME,
            duration_unit=TimeDuration.TimeUnitChoices.MINUTES,
        )

        interval1 = create_interval(
            duration_value=5,
            duration_type=BaseDuration.DurationType.DISTANCE,
            duration_unit=DistanceDuration.DistanceUnitChoices.MILES,
            interval_type=Interval.IntervalType.ACTIVE,
            parent=warmup1,
        )

        repeat1 = create_repeat(
            interval=interval1,
            repititions=3,
            rest_interval=warmup1,
        )

        cooldown1 = create_cool_down(
            duration_value=5,
            duration_type=BaseDuration.DurationType.TIME,
            duration_unit=TimeDuration.TimeUnitChoices.MINUTES,
            parent=repeat1,
        )

        workout1 = build_workout(
            author=author,
            title="Morning Routine",
            description="A simple morning workout routine",
            workout_type=Workout.WorkoutType.RUN,  # Adjust based on your available types
            intervals=[warmup1, interval1, repeat1, cooldown1],
        )

        # Create the second workout
        warmup2 = create_warmup(
            duration_value=15,
            duration_type=BaseDuration.DurationType.TIME,
            duration_unit=TimeDuration.TimeUnitChoices.MINUTES,
        )

        interval2 = create_interval(
            duration_value=30,
            duration_type=BaseDuration.DurationType.POWER,
            duration_unit=PowerDuration.PowerUnitChoices.WATTS,
            interval_type=Interval.IntervalType.ACTIVE,
            parent=warmup2,
        )

        repeat2 = create_repeat(
            interval=interval2,
            repititions=5,
            rest_interval=warmup2,
        )

        cooldown2 = create_cool_down(
            duration_value=10,
            duration_type=BaseDuration.DurationType.TIME,
            duration_unit=TimeDuration.TimeUnitChoices.MINUTES,
            parent=repeat2,
        )

        workout2 = build_workout(
            author=author,
            title="Evening Cardio",
            description="An evening cardio workout session",
            workout_type=Workout.WorkoutType.CYCLE,  # Adjust based on your available types
            intervals=[warmup2, interval2, repeat2, cooldown2],
        )

        self.stdout.write(self.style.SUCCESS("Seed data has been added."))

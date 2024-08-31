from django.db import models, transaction
from django.contrib.auth.models import User

from workouts.models.interval import Interval


class Workout(models.Model):

    class WorkoutType(models.IntegerChoices):
        RUN = 1, "Run"
        SWIM = 2, "Swim"
        CYCLE = 3, "Cycle"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    workout_type = models.PositiveSmallIntegerField(
        choices=WorkoutType.choices, default=WorkoutType.RUN
    )
    first_interval = models.OneToOneField(
        Interval,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="workout_first_interval",
    )
    last_interval = models.OneToOneField(
        Interval,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="workout_last_interval",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def intervals(self):
        intervals = []

        interval = self.last_interval
        while interval:
            intervals.append(interval)
            interval = interval.parent

        return list(reversed(intervals))

    def __str__(self):
        return self.title


def build_workout(
    author: User,
    title: str,
    description: str,
    workout_type: Workout.WorkoutType,
    first_interval: Interval,
    last_interval: Interval,
) -> Workout:
    """
    Build a workout with the specified first and last intervals.

    Args:
        author (User): The user creating the workout.
        title (str): The title of the workout.
        description (str): A brief description of the workout.
        workout_type (Workout.WorkoutType): The type of workout (Run, Swim, Cycle).
        first_interval (Interval): The first interval in the workout.
        last_interval (Interval): The last interval in the workout.

    Returns:
        Workout: The created workout instance.
    """
    with transaction.atomic():
        workout = Workout.objects.create(
            author=author,
            title=title,
            description=description,
            workout_type=workout_type,
            first_interval=first_interval,
            last_interval=last_interval,
        )

        workout.save()

    return workout

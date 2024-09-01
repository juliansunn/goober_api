from typing import Optional, Union
from django.db import transaction
from workouts.models.duration import (
    BaseDuration,
    CaloricDuration,
    DistanceDuration,
    HeartRateDuration,
    PowerDuration,
    TimeDuration,
)
from workouts.models.interval import Interval

from django.contrib.auth.models import User

from workouts.models.workout import Workout


def create_warmup(
    duration_value: int,
    duration_type: BaseDuration.DurationType,
    duration_unit: Union[
        TimeDuration.TimeUnitChoices,
        DistanceDuration.DistanceUnitChoices,
        PowerDuration.PowerUnitChoices,
        CaloricDuration.CaloricUnitChoices,
        HeartRateDuration.HeartRateUnitChoices,
    ],
) -> Interval:
    """Create a warm-up interval with the given duration and order."""
    model = BaseDuration.get_duration_model(duration_type)
    warmup_duration = model.objects.create(value=duration_value, unit=duration_unit)
    warmup_interval = Interval.objects.create(
        type=Interval.IntervalType.WARMUP,
        duration=warmup_duration,
    )
    return warmup_interval


def create_cool_down(
    duration_value: int,
    duration_type: BaseDuration.DurationType,
    duration_unit: Union[
        TimeDuration.TimeUnitChoices,
        DistanceDuration.DistanceUnitChoices,
        PowerDuration.PowerUnitChoices,
        CaloricDuration.CaloricUnitChoices,
        HeartRateDuration.HeartRateUnitChoices,
    ],
    parent: Optional[int] = None,
) -> Interval:
    """Create a cool-down interval with the given duration and order."""
    model = BaseDuration.get_duration_model(duration_type)
    cool_down_duration = model.objects.create(value=duration_value, unit=duration_unit)
    cool_down_interval = Interval.objects.create(
        type=Interval.IntervalType.COOLDOWN,
        duration=cool_down_duration,
    )
    if parent:
        cool_down_interval.parent = parent.pk
        cool_down_interval.save()
    return cool_down_interval


def create_interval(
    duration_value: int,
    duration_type: BaseDuration.DurationType,
    duration_unit: Union[
        TimeDuration.TimeUnitChoices,
        DistanceDuration.DistanceUnitChoices,
        PowerDuration.PowerUnitChoices,
        CaloricDuration.CaloricUnitChoices,
        HeartRateDuration.HeartRateUnitChoices,
    ],
    interval_type: Interval.IntervalType,
    parent: Optional[int] = None,
) -> Interval:
    """Create an interval with the given duration and order."""
    model = BaseDuration.get_duration_model(duration_type)
    interval_duration = model.objects.create(value=duration_value, unit=duration_unit)
    interval = Interval.objects.create(type=interval_type, duration=interval_duration)
    if parent:
        interval.parent = parent.pk
        interval.save()
    return interval


def create_repeat(
    interval: Interval,
    repititions: int = 2,
    rest_interval: Interval = None,
) -> Interval:
    """Create a repeat interval with the given duration and order."""

    interval.repititions = repititions
    interval.rest_interval = rest_interval
    interval.save()

    return interval


def build_workout(
    author: User,
    title: str,
    description: str,
    workout_type: Workout.WorkoutType,
    intervals: list[Interval],
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
        )
        if intervals:
            workout.intervals.add(*intervals)

    return workout

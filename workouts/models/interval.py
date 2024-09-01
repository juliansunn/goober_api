from typing import Union
from django.db import models

# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey

from polymorphic.models import PolymorphicModel

from workouts.models.duration import (
    BaseDuration,
    CaloricDuration,
    DistanceDuration,
    HeartRateDuration,
    PowerDuration,
    TimeDuration,
)


EFFORT_CHOICES = [(i, f"{i}/10") for i in range(1, 11)]


class BaseInterval(PolymorphicModel):

    class IntervalType(models.IntegerChoices):
        WARMUP = 1, "Warm-up"
        COOLDOWN = 2, "Cool-down"
        ACTIVE = 3, "Active"
        REST = 4, "Rest"

    type = models.IntegerField(
        choices=IntervalType.choices, default=IntervalType.ACTIVE
    )

    # Generic ForeignKey to handle relationships with any Duration type
    # duration_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # duration_id = models.PositiveIntegerField()
    # duration = GenericForeignKey("duration_type", "duration_id")

    duration = models.ForeignKey(
        BaseDuration, on_delete=models.CASCADE, related_name="intervals"
    )

    perceived_effort = models.PositiveSmallIntegerField(
        choices=EFFORT_CHOICES, blank=True, null=True
    )
    parent = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="This will serve as a pointer to the parent intervals PK.",
    )

    def delete(self, *args, **kwargs):
        # link the parent to the next interval

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.type} - {self.duration}"


class Interval(BaseInterval):
    pass


class Repeat(BaseInterval):
    repititions = models.PositiveIntegerField(default=1)
    rest_interval = models.OneToOneField(
        "Interval", on_delete=models.CASCADE, related_name="repeat_interval", null=True
    )


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
) -> Interval:
    """Create a cool-down interval with the given duration and order."""
    model = BaseDuration.get_duration_model(duration_type)
    cool_down_duration = model.objects.create(value=duration_value, unit=duration_unit)
    cool_down_interval = Interval.objects.create(
        type=Interval.IntervalType.COOLDOWN,
        duration=cool_down_duration,
    )
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
    parent: Interval = None,
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
    repititions: int = 2,
    rest_interval: Interval = None,
    parent: Interval = None,
) -> Interval:
    """Create a repeat interval with the given duration and order."""
    model = BaseDuration.get_duration_model(duration_type)
    interval_duration = model.objects.create(value=duration_value, unit=duration_unit)
    repeat = Repeat.objects.create(
        duration=interval_duration,
        type=interval_type,
        repititions=repititions,
        rest_interval=rest_interval,
    )
    if parent:
        repeat.parent = parent.pk
        repeat.save()

    return repeat

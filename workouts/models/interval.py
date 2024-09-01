from typing import Optional, Union
from django.db import models


from workouts.models.duration import (
    BaseDuration,
    CaloricDuration,
    DistanceDuration,
    HeartRateDuration,
    PowerDuration,
    TimeDuration,
)


EFFORT_CHOICES = [(i, f"{i}/10") for i in range(1, 11)]


class Interval(models.Model):

    class IntervalType(models.IntegerChoices):
        WARMUP = 1, "Warm-up"
        COOLDOWN = 2, "Cool-down"
        ACTIVE = 3, "Active"
        REST = 4, "Rest"

    type = models.IntegerField(
        choices=IntervalType.choices, default=IntervalType.ACTIVE
    )

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
    repititions = models.PositiveIntegerField(default=0, blank=True, null=True)
    rest_interval = models.OneToOneField(
        "Interval", on_delete=models.CASCADE, related_name="repeat_interval", null=True
    )

    def is_repeat(self) -> bool:
        return self.repititions > 0

    def delete(self, *args, **kwargs):
        # link the parent to the next interval

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.type} - {self.duration}"

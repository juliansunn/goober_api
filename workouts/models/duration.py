from enum import Enum
from django.db import models


class DurationType(Enum):
    DISTANCE = 1
    TIME = 2
    CALORIC = 3
    HEART_RATE = 4
    POWER = 5


class BaseDuration(models.Model):

    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.value} {self.unit}"

    @property
    def unit(self):
        raise NotImplementedError

    @staticmethod
    def get_duration_model(duration_type: DurationType):
        duration_mapping = {
            DurationType.DISTANCE: DistanceDuration,
            DurationType.TIME: TimeDuration,
            DurationType.CALORIC: CaloricDuration,
            DurationType.HEART_RATE: HeartRateDuration,
            DurationType.POWER: PowerDuration,
        }
        return duration_mapping.get(duration_type)


class DistanceDuration(BaseDuration):

    class DistanceUnitChoices(models.IntegerChoices):
        MILES = 1, "Miles"
        KILOMETERS = 2, "Kilometers"
        METERS = 3, "Meters"

    unit = models.PositiveSmallIntegerField(
        choices=DistanceUnitChoices.choices, default=DistanceUnitChoices.MILES
    )


class TimeDuration(BaseDuration):

    class TimeUnitChoices(models.IntegerChoices):
        SECONDS = 1, "Seconds"
        MINUTES = 2, "Minutes"
        HOURS = 3, "Hours"

    unit = models.PositiveSmallIntegerField(
        choices=TimeUnitChoices.choices, default=TimeUnitChoices.MINUTES
    )

    def converted_value(self):
        if self.unit == self.TimeUnitChoices.SECONDS:
            return self.value / 60
        elif self.unit == self.TimeUnitChoices.MINUTES:
            return self.value
        elif self.unit == self.TimeUnitChoices.HOURS:
            return self.value * 60


class CaloricDuration(BaseDuration):

    class CaloricUnitChoices(models.IntegerChoices):
        CALORIES = 1, "Calories"
        KJ = 2, "Kilocalories"

    unit = models.PositiveSmallIntegerField(
        choices=CaloricUnitChoices, default=CaloricUnitChoices.CALORIES
    )


class HeartRateDuration(BaseDuration):

    class HeartRateUnitChoices(models.IntegerChoices):
        BPM = 1, "Beats Per Minute"
        PERCENT = 2, "Percentage"

    unit = models.PositiveSmallIntegerField(
        choices=HeartRateUnitChoices, default=HeartRateUnitChoices.BPM
    )


class PowerDuration(BaseDuration):

    class PowerUnitChoices(models.IntegerChoices):
        WATTS = 1, "Watts"
        KJ = 2, "Kilowatts"

    unit = models.PositiveSmallIntegerField(
        choices=PowerUnitChoices, default=PowerUnitChoices.WATTS
    )

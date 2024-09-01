from django.db import models
from polymorphic.models import PolymorphicModel


class BaseDuration(PolymorphicModel):

    class DurationType(models.IntegerChoices):
        DISTANCE = 1, "DISTANCE"
        TIME = 2, "TIME"
        CALORIC = 3, "CALORIC"
        HEART_RATE = 4, "HEART_RATE"
        POWER = 5, "POWER"

    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.value} {self.unit}"

    @property
    def unit(self):
        raise NotImplementedError

    @staticmethod
    def get_duration_model(duration_type: DurationType):
        duration_mapping = {
            BaseDuration.DurationType.DISTANCE: DistanceDuration,
            BaseDuration.DurationType.TIME: TimeDuration,
            BaseDuration.DurationType.CALORIC: CaloricDuration,
            BaseDuration.DurationType.HEART_RATE: HeartRateDuration,
            BaseDuration.DurationType.POWER: PowerDuration,
        }
        return duration_mapping.get(duration_type)


class DistanceDuration(BaseDuration):
    duration_string = BaseDuration.DurationType.DISTANCE.name

    class DistanceUnitChoices(models.IntegerChoices):
        MILES = 1, "Miles"
        KILOMETERS = 2, "Kilometers"
        METERS = 3, "Meters"

    unit = models.PositiveSmallIntegerField(
        choices=DistanceUnitChoices.choices, default=DistanceUnitChoices.MILES
    )


class TimeDuration(BaseDuration):
    duration_string = BaseDuration.DurationType.TIME.name

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
    duration_string = BaseDuration.DurationType.CALORIC.name

    class CaloricUnitChoices(models.IntegerChoices):
        CALORIES = 1, "Calories"
        KJ = 2, "Kilocalories"

    unit = models.PositiveSmallIntegerField(
        choices=CaloricUnitChoices, default=CaloricUnitChoices.CALORIES
    )


class HeartRateDuration(BaseDuration):
    duration_string = BaseDuration.DurationType.HEART_RATE.name

    class HeartRateUnitChoices(models.IntegerChoices):
        BPM = 1, "Beats Per Minute"
        PERCENT = 2, "Percentage"

    unit = models.PositiveSmallIntegerField(
        choices=HeartRateUnitChoices, default=HeartRateUnitChoices.BPM
    )


class PowerDuration(BaseDuration):
    duration_string = BaseDuration.DurationType.POWER.name

    class PowerUnitChoices(models.IntegerChoices):
        WATTS = 1, "Watts"
        KJ = 2, "Kilowatts"

    unit = models.PositiveSmallIntegerField(
        choices=PowerUnitChoices, default=PowerUnitChoices.WATTS
    )

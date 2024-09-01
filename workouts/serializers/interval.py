from rest_framework import serializers
from workouts.models import Interval
from workouts.models.duration import BaseDuration


class DurationSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField()

    class Meta:
        model = BaseDuration
        fields = ["value", "unit"]

    def get_unit(self, obj: BaseDuration):
        return obj.unit


class IntervalSerializer(serializers.ModelSerializer):
    duration = DurationSerializer()
    type = serializers.SerializerMethodField()
    is_repeat = serializers.SerializerMethodField()
    repititions = serializers.SerializerMethodField()
    rest_interval = serializers.SerializerMethodField()

    class Meta:
        model = Interval
        fields = [
            "id",
            "type",
            "duration",
            "perceived_effort",
            "parent",
            "is_repeat",
            "repititions",
            "rest_interval",
        ]

    def get_type(self, obj: Interval):
        return obj.duration.duration_string

    def get_is_repeat(self, obj: Interval):
        return obj.is_repeat()

    def get_repititions(self, obj: Interval):
        if not obj.is_repeat():
            return None
        return obj.repititions

    def get_rest_interval(self, obj: Interval):
        if not obj.is_repeat():
            return None
        return IntervalSerializer(obj.rest_interval).data

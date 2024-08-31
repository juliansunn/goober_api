from rest_framework import serializers
from workouts.models import Interval


class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interval
        fields = "__all__"

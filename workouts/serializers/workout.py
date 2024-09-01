from rest_framework import serializers

from workouts.models.workout import Workout
from django.contrib.auth.models import User

from workouts.serializers.interval import IntervalSerializer


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        read_only_fields = (
            "created_at",
            "updated_at",
        )
        fields = "__all__"

    title = serializers.CharField()
    description = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    intervals = serializers.SerializerMethodField()

    def get_intervals(self, obj: Workout):
        return IntervalSerializer(obj.sorted_intervals, many=True).data

    def create(self, validated_data):
        return Workout.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.author = validated_data.get("author", instance.author)
        instance.save()
        return instance

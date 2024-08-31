from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from workouts.models import Workout
from workouts.serializers import WorkoutSerializer
from rest_framework.response import Response


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        workout = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(workout)
        return Response(serializer.data)

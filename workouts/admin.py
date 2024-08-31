from django.contrib import admin

from .models import Workout


# Admin classes
@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")

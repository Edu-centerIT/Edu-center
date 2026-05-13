

# Register your models here.
from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'student', 'is_present', 'recorded_at']
    list_filter = ['is_present', 'recorded_at']
    search_fields = ['student__first_name', 'lesson__id']#пошук
    readonly_fields = ['recorded_at']



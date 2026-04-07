from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Lesson, LessonTemplate


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'subject', 'date', 'start_time', 'status']
    list_filter = ['status', 'date', 'lesson_type']
    search_fields = ['teacher__first_name', 'subject__name']
    readonly_fields = ['created_at']


@admin.register(LessonTemplate)
class LessonTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'subject', 'lesson_type', 'status']
    list_filter = ['status', 'lesson_type']
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Parent


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'branch', 'status']
    list_filter = ['status', 'branch']
    search_fields = ['first_name', 'last_name']


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student', 'phone']
    search_fields = ['name', 'phone']
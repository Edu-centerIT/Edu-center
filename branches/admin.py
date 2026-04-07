from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'status', 'created_at']
    list_filter = ['status', 'city']
    search_fields = ['name', 'city']
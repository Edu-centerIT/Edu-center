from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Group, GroupMembership


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'status']
    list_filter = ['status', 'branch']
    inlines = [GroupMembershipInline]
from django.contrib import admin

# Register your models here.
from .models import Group, GroupMembership

#Inline = можливість редагувати пов’язані об’єкти прямо всередині іншого
class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership #у групи є пов’язані membership-и — показуй їх
    extra = 1 #пустий рядок, можна було одразу додати нового студента


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'status']
    list_filter = ['status', 'branch']
    inlines = [GroupMembershipInline] #Показуй учасників групи прямо всередині сторінки групи
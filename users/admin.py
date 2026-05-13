from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма для створення користувача"""
    
    class Meta:
        model = CustomUser
        fields = ('phone', 'email', 'first_name', 'last_name', 'role')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Встановити username = phone
        user.username = user.phone
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Форма для редагування користувача"""
    
    class Meta:
        model = CustomUser
        fields = ('phone', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Синхронізувати username = phone
        user.username = user.phone
        if commit:
            user.save()
        return user


class CustomUserAdmin(BaseUserAdmin):
    """
    Розширена форма адміністратора для CustomUser
    """
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    # Поля для списку користувачів
    list_display = ('phone', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('phone', 'first_name', 'last_name', 'email')
    ordering = ('phone',)
    
    # Поля для редагування
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Custom Fields', {'fields': ('role',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Поля для створення нового користувача
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Custom Fields', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
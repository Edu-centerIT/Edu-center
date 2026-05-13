from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Кастомний UserManager для CustomUser з phone як USERNAME_FIELD
    """
    
    def create_user(self, phone, email=None, password=None, **extra_fields):
        """
        Створити звичайного користувача
        """
        if not phone:
            raise ValueError('The Phone field must be set')
        
        email = self.normalize_email(email) if email else ''
        user = self.model(phone=phone, email=email, **extra_fields)
        user.username = phone  # Синхронізуємо username = phone
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        """
        Створити суперпользувача
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Розширена модель користувача з phone як основним полем для входу
    """
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
    ]
    
    # ✅ БАЗОВІ ПОЛЯ (успадковані від AbstractUser)
    # username - автоматично синхронізується з phone
    # email - VARCHAR(255)
    # first_name - VARCHAR(150)
    # last_name - VARCHAR(150)
    # password - VARCHAR(128)
    # last_login - DATETIME
    # date_joined - DATETIME
    # is_superuser - BOOLEAN
    # is_staff - BOOLEAN
    
    # ✅ КАСТОМНІ ПОЛЯ
    phone = models.CharField(
        max_length=15,
        unique=True,
        help_text="Phone number in format: +380XXXXXXXXX"
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='TEACHER',
        help_text="User role: ADMIN or TEACHER"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active"
    )
    
    # ✅ НАЛАШТУВАННЯ АУТЕНТИФІКАЦІЇ
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    
    # ✅ КАСТОМНИЙ MANAGER
    objects = CustomUserManager()
    
    # ✅ МЕТА-ІНФОРМАЦІЯ
    class Meta:
        db_table = 'users_customuser'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        ordering = ['phone']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def save(self, *args, **kwargs):
        """
        Автоматично синхронізувати username = phone перед збереженням
        """
        if self.phone:
            self.username = self.phone
        super().save(*args, **kwargs)
    
    def __str__(self):
        """Строкове представлення користувача"""
        return f"{self.first_name} {self.last_name} ({self.phone})"
    
    # ✅ ДОПОМІЖНІ МЕТОДИ
    
    def get_full_name(self):
        """Отримати повне ім'я користувача"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Отримати скорочене ім'я (лише ім'я)"""
        return self.first_name.strip()
    
    def is_admin(self):
        """Перевірити, чи користувач адміністратор"""
        return self.role == 'ADMIN'
    
    def is_teacher(self):
        """Перевірити, чи користувач вчитель"""
        return self.role == 'TEACHER'
    
    def can_create_lessons(self):
        """Перевірити, чи користувач може створювати уроки"""
        return self.is_teacher() and self.is_active
    
    def can_manage_students(self):
        """Перевірити, чи користувач може управляти студентами"""
        return self.is_admin() and self.is_active
    
    @property
    def is_online(self):
        """Перевірити, чи користувач онлайн (за останнім входом)"""
        if self.last_login:
            from datetime import timedelta
            from django.utils import timezone
            return (timezone.now() - self.last_login) < timedelta(minutes=30)
        return False

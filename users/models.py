from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
    ]
    
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='TEACHER')
    is_active = models.BooleanField(default=True)
    
    # ✅ Залишаємо username за замовчуванням, але використовуємо phone для входу
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    
    def save(self, *args, **kwargs):
        # ✅ Автоматично синхронізувати username = phone
        if self.phone:
            self.username = self.phone
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from branches.models import Branch 

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Parent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='parent')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    relationship = models.CharField(max_length=50)
    
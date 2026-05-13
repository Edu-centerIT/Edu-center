from django.db import models
from branches.models import Branch 
from students.models import Student  

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE) #CASCADE-branch видалили — всі пов’язані записи теж
    students = models.ManyToManyField(Student, through='GroupMembership')
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active' #значення поля за замовчуванням
    )
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
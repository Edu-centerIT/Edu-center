from django.db import models
from branches.models import Branch,Student

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through='GroupMembership')
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
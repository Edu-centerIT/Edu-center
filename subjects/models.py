from django.db import models
from branches.models import Branch 

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('name', 'branch')
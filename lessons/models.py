from django.db import models

from branches.models import Branch
from subjects.models import Subject  
from students.models import Student  

from django.contrib.auth import get_user_model

from groups.models import Group

CustomUser = get_user_model()


# Create your models here.
class LessonTemplate(models.Model): #правило, за яким уроки створюються
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=10, choices=[('individual', 'Individual'), ('group', 'Group')])
    
    # For individual lessons
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    
    # For group lessons
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    
    # Розклад
    days_of_week = models.CharField(max_length=50)  # e.g., "1,3,5" for Mon, Wed, Fri
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active' #значення поля за замовчуванням
    )

class Lesson(models.Model):
    LESSON_STATUS = [
        ('SCHEDULED', 'Scheduled'), #запланований
        ('COMPLETED', 'Completed'), #проведений
        ('CANCELLED', 'Cancelled'), #скасований
    ]
    
    template = models.ForeignKey(LessonTemplate, on_delete=models.SET_NULL, null=True, blank=True) #якщо шаблон видалити → урок залишиться
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    lesson_type = models.CharField(max_length=10, choices=[('individual', 'Individual'), ('group', 'Group')])
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    status = models.CharField(max_length=20, choices=LESSON_STATUS, default='SCHEDULED') #'SCHEDULED' по дефолту урок ще не проведений
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True автоматично поставити дату і час тільки один раз — при створенні запису
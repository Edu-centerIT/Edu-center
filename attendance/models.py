from django.db import models
from django.contrib.auth import get_user_model
from lessons.models import Lesson
from students.models import Student

CustomUser = get_user_model()

# Create your models here.
class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendance_records') #CASCADE-урок видалили — всі пов’язані записи теж
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField()
    notes = models.TextField(blank=True) #blank=True можна залишити порожнім
    
    # Ось сюди ми перенесли поле created_at:
    created_at = models.DateTimeField(auto_now_add=True) 
    
    recorded_at = models.DateTimeField(auto_now=True) #автоматично оновлюється кожного разу при збереженні
    
    class Meta:
        unique_together = ('lesson', 'student')#Комбінація має бути унікальною
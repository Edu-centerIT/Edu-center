from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from lessons.models import Lesson
from students.models import Student


CustomUser = get_user_model()

  # ✅ З subjects
from students.models import Student 
# Create your models here.
class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField()
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('lesson', 'student')
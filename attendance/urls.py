from django.urls import path
from . import views

urlpatterns = [
    path('lesson/<int:lesson_id>/', views.lesson_attendance, name='lesson_attendance'),
    path('student/<int:student_id>/', views.student_attendance_history, name='student_attendance_history'),
]

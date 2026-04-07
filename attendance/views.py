from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Attendance
from lessons.models import Lesson
from students.models import Student
from groups.models import GroupMembership


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def lesson_attendance(request, lesson_id):
    """Позначити відвідування для уроку"""
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    
    # Дозволити вчителю уроку або адміністратору
    if not (request.user == lesson.teacher or request.user.role == 'ADMIN'):
        messages.error(request, 'Access denied')
        return redirect('lesson_detail', pk=lesson.pk)
    
    # Отримуємо студентів, які повинні бути на цьому уроці
    if lesson.lesson_type == 'individual':
        students = [lesson.student]
    else:  # group
        memberships = GroupMembership.objects.filter(group=lesson.group, left_at__isnull=True)
        students = [m.student for m in memberships]
    
    if request.method == 'POST':
        for student in students:
            is_present = request.POST.get(f'is_present_{student.id}') == 'on'
            notes = request.POST.get(f'notes_{student.id}', '').strip()
            
            # Обновити або створити запис
            attendance, created = Attendance.objects.update_or_create(
                lesson=lesson,
                student=student,
                defaults={
                    'is_present': is_present,
                    'notes': notes
                }
            )
        
        # Позначити урок як завершений
        lesson.status = 'COMPLETED'
        lesson.save()
        
        messages.success(request, 'Attendance marked successfully')
        return redirect('lesson_detail', pk=lesson.pk)
    
    # Отримуємо поточні записи про відвідування
    attendance_records = Attendance.objects.filter(lesson=lesson)
    attendance_dict = {a.student_id: a for a in attendance_records}
    
    # Готуємо дані для шаблону
    student_attendance = []
    for student in students:
        attendance = attendance_dict.get(student.id)
        student_attendance.append({
            'student': student,
            'attendance': attendance
        })
    
    context = {
        'lesson': lesson,
        'student_attendance': student_attendance,
    }
    return render(request, 'attendance/lesson_attendance.html', context)


@login_required(login_url='login')
def student_attendance_history(request, student_id):
    """Історія відвідування студента"""
    if not (request.user.role == 'ADMIN'):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, pk=student_id)
    attendance_records = Attendance.objects.filter(student=student).select_related('lesson').order_by('-lesson__date')
    
    # Статистика
    total = attendance_records.count()
    attended = attendance_records.filter(is_present=True).count()
    missed = total - attended
    percentage = (attended / total * 100) if total > 0 else 0
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'total': total,
        'attended': attended,
        'missed': missed,
        'percentage': round(percentage, 1),
    }
    return render(request, 'attendance/student_attendance_history.html', context)
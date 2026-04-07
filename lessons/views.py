from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Lesson
from .services import check_teacher_conflict, check_student_conflict, check_group_conflicts
from branches.models import Branch
from subjects.models import Subject
from students.models import Student
from groups.models import Group, GroupMembership
from users.models import CustomUser


def check_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'


@login_required(login_url='login')
def lesson_list(request):
    """Список уроків"""
    if not check_admin(request.user) and request.user.role != 'TEACHER':
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    lessons = Lesson.objects.filter(status='SCHEDULED').order_by('date', 'start_time')
    
    # Для вчителя показуємо тільки його уроки
    if request.user.role == 'TEACHER':
        lessons = lessons.filter(teacher=request.user)
    
    # Фільтрація
    teacher_id = request.GET.get('teacher')
    branch_id = request.GET.get('branch')
    status = request.GET.get('status', 'SCHEDULED')
    
    if teacher_id:
        lessons = lessons.filter(teacher_id=teacher_id)
    if branch_id:
        lessons = lessons.filter(branch_id=branch_id)
    if status:
        lessons = Lesson.objects.filter(status=status).order_by('date', 'start_time')
    
    teachers = CustomUser.objects.filter(role='TEACHER')
    branches = Branch.objects.filter(status='active')
    
    context = {
        'lessons': lessons,
        'teachers': teachers,
        'branches': branches,
        'selected_teacher': teacher_id,
        'selected_branch': branch_id,
        'selected_status': status,
    }
    return render(request, 'lessons/lesson_list.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def lesson_create(request):
    """Створити новий урок"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    if request.method == 'POST':
        lesson_type = request.POST.get('lesson_type')
        teacher_id = request.POST.get('teacher')
        subject_id = request.POST.get('subject')
        branch_id = request.POST.get('branch')
        date_str = request.POST.get('date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        # Валідація
        errors = []
        if not all([lesson_type, teacher_id, subject_id, branch_id, date_str, start_time_str, end_time_str]):
            errors.append('All fields are required')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'lessons/lesson_form.html', get_context(request))
        
        try:
            lesson_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Invalid date or time format')
            return render(request, 'lessons/lesson_form.html', get_context(request))
        
        if start_time >= end_time:
            messages.error(request, 'Start time must be before end time')
            return render(request, 'lessons/lesson_form.html', get_context(request))
        
        teacher = get_object_or_404(CustomUser, pk=teacher_id, role='TEACHER')
        subject = get_object_or_404(Subject, pk=subject_id)
        branch = get_object_or_404(Branch, pk=branch_id)
        
        # Перевірка конфліктів вчителя
        is_valid, error = check_teacher_conflict(teacher, lesson_date, start_time, end_time)
        if not is_valid:
            messages.error(request, f'Conflict: {error}')
            return render(request, 'lessons/lesson_form.html', get_context(request))
        
        if lesson_type == 'individual':
            student_id = request.POST.get('student')
            if not student_id:
                messages.error(request, 'Student is required for individual lesson')
                return render(request, 'lessons/lesson_form.html', get_context(request))
            
            student = get_object_or_404(Student, pk=student_id, branch=branch)
            
            # Перевірка конфліктів студента
            is_valid, error = check_student_conflict(student, lesson_date, start_time, end_time)
            if not is_valid:
                messages.error(request, f'Student conflict: {error}')
                return render(request, 'lessons/lesson_form.html', get_context(request))
            
            lesson = Lesson.objects.create(
                teacher=teacher,
                subject=subject,
                branch=branch,
                lesson_type='individual',
                student=student,
                date=lesson_date,
                start_time=start_time,
                end_time=end_time,
                status='SCHEDULED'
            )
        
        elif lesson_type == 'group':
            group_id = request.POST.get('group')
            if not group_id:
                messages.error(request, 'Group is required for group lesson')
                return render(request, 'lessons/lesson_form.html', get_context(request))
            
            group = get_object_or_404(Group, pk=group_id, branch=branch)
            
            # Перевірка конфліктів для всіх членів групи
            is_valid, error = check_group_conflicts(group, lesson_date, start_time, end_time)
            if not is_valid:
                messages.error(request, f'Group member conflict: {error}')
                return render(request, 'lessons/lesson_form.html', get_context(request))
            
            lesson = Lesson.objects.create(
                teacher=teacher,
                subject=subject,
                branch=branch,
                lesson_type='group',
                group=group,
                date=lesson_date,
                start_time=start_time,
                end_time=end_time,
                status='SCHEDULED'
            )
        
        messages.success(request, f'Lesson created successfully')
        return redirect('lesson_detail', pk=lesson.pk)
    
    context = get_context(request)
    return render(request, 'lessons/lesson_form.html', context)


@login_required(login_url='login')
def lesson_detail(request, pk):
    """Деталі уроку"""
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if not check_admin(request.user) and request.user != lesson.teacher:
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    context = {'lesson': lesson}
    return render(request, 'lessons/lesson_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def lesson_edit(request, pk):
    """Редагувати урок"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if lesson.status != 'SCHEDULED':
        messages.error(request, 'Can only edit scheduled lessons')
        return redirect('lesson_detail', pk=lesson.pk)
    
    if request.method == 'POST':
        # Отримуємо нові значення
        teacher_id = request.POST.get('teacher')
        subject_id = request.POST.get('subject')
        date_str = request.POST.get('date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        try:
            lesson_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Invalid date or time format')
            return render(request, 'lessons/lesson_form.html', {
                'lesson': lesson,
                **get_context(request)
            })
        
        teacher = get_object_or_404(CustomUser, pk=teacher_id)
        subject = get_object_or_404(Subject, pk=subject_id)
        
        # Перевірка конфліктів (виключаючи поточний урок)
        is_valid, error = check_teacher_conflict(teacher, lesson_date, start_time, end_time, exclude_lesson=lesson)
        if not is_valid:
            messages.error(request, f'Conflict: {error}')
            return render(request, 'lessons/lesson_form.html', {
                'lesson': lesson,
                **get_context(request)
            })
        
        lesson.teacher = teacher
        lesson.subject = subject
        lesson.date = lesson_date
        lesson.start_time = start_time
        lesson.end_time = end_time
        lesson.save()
        
        messages.success(request, 'Lesson updated')
        return redirect('lesson_detail', pk=lesson.pk)
    
    context = {
        'lesson': lesson,
        **get_context(request)
    }
    return render(request, 'lessons/lesson_form.html', context)


@login_required(login_url='login')
def lesson_cancel(request, pk):
    """Скасувати урок"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    lesson = get_object_or_404(Lesson, pk=pk)
    lesson.status = 'CANCELLED'
    lesson.save()
    
    messages.success(request, 'Lesson cancelled')
    return redirect('lesson_list')


def get_context(request):
    """Допоміжна функція для отримання контексту"""
    return {
        'teachers': CustomUser.objects.filter(role='TEACHER'),
        'subjects': Subject.objects.filter(status='active'),
        'branches': Branch.objects.filter(status='active'),
        'students': Student.objects.filter(status='active'),
        'groups': Group.objects.filter(status='active'),
    }


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from branches.models import Branch
from lessons.models import Lesson
from students.models import Student
from datetime import datetime, timedelta


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Логін з номером телефону
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not phone or not password:
            messages.error(request, 'Please enter phone and password')
            return render(request, 'users/login.html')
        
        user = authenticate(request, username=phone, password=password)
        
        if user is not None:
            if not user.is_active:
                messages.error(request, 'Your account is inactive')
                return render(request, 'users/login.html')
            
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid phone number or password')
    
    return render(request, 'users/login.html')


@login_required(login_url='login')
def logout_view(request):
    """
    Вихід користувача
    """
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """
    Головна сторінка - різна для ADMIN і TEACHER
    """
    context = {
        'user': request.user,
        'role': request.user.role,
    }
    
    if request.user.role == 'ADMIN':
        # Для адміністратора показуємо статистику
        context['branches_count'] = Branch.objects.filter(status='active').count()
        context['students_count'] = Student.objects.filter(status='active').count()
        context['lessons_count'] = Lesson.objects.filter(status='SCHEDULED').count()
        context['branches'] = Branch.objects.filter(status='active')[:5]
        return render(request, 'users/admin_dashboard.html', context)
    
    elif request.user.role == 'TEACHER':
        # Для вчителя показуємо його уроки на цей тиждень
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        context['lessons'] = Lesson.objects.filter(
            teacher=request.user,
            date__gte=week_start,
            date__lte=week_end,
            status='SCHEDULED'
        ).order_by('date', 'start_time')
        
        return render(request, 'users/teacher_dashboard.html', context)
    
    return render(request, 'users/dashboard.html', context)
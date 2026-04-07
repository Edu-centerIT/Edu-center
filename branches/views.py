from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Branch
from lessons.models import Lesson
from students.models import Student


def check_admin(user):
    """Перевірити, чи користувач адміністратор"""
    return user.is_authenticated and user.role == 'ADMIN'


@login_required(login_url='login')
def branch_list(request):
    """Список всіх філій"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branches = Branch.objects.filter(status='active').order_by('name')
    archived = Branch.objects.filter(status='archived').count()
    
    context = {
        'branches': branches,
        'archived_count': archived,
    }
    return render(request, 'branches/branch_list.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def branch_create(request):
    """Створити нову філію"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        
        if not name or not address or not city:
            messages.error(request, 'All fields are required')
            return render(request, 'branches/branch_form.html')
        
        if Branch.objects.filter(name=name).exists():
            messages.error(request, 'Branch with this name already exists')
            return render(request, 'branches/branch_form.html')
        
        branch = Branch.objects.create(
            name=name,
            address=address,
            city=city,
            status='active'
        )
        messages.success(request, f'Branch "{branch.name}" created successfully')
        return redirect('branch_detail', pk=branch.pk)
    
    return render(request, 'branches/branch_form.html')


@login_required(login_url='login')
def branch_detail(request, pk):
    """Деталі філії"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branch = get_object_or_404(Branch, pk=pk)
    
    context = {
        'branch': branch,
        'students_count': Student.objects.filter(branch=branch, status='active').count(),
        'lessons_count': Lesson.objects.filter(branch=branch, status='SCHEDULED').count(),
    }
    return render(request, 'branches/branch_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def branch_edit(request, pk):
    """Редагувати філію"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branch = get_object_or_404(Branch, pk=pk)
    
    if request.method == 'POST':
        branch.name = request.POST.get('name', '').strip()
        branch.address = request.POST.get('address', '').strip()
        branch.city = request.POST.get('city', '').strip()
        
        if not branch.name or not branch.address or not branch.city:
            messages.error(request, 'All fields are required')
            return render(request, 'branches/branch_form.html', {'branch': branch})
        
        branch.save()
        messages.success(request, 'Branch updated successfully')
        return redirect('branch_detail', pk=branch.pk)
    
    context = {'branch': branch}
    return render(request, 'branches/branch_form.html', context)


@login_required(login_url='login')
def branch_archive(request, pk):
    """Архівувати філію"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branch = get_object_or_404(Branch, pk=pk)
    
    # Перевірити, чи є активні студенти або уроки
    active_students = Student.objects.filter(branch=branch, status='active').count()
    active_lessons = Lesson.objects.filter(branch=branch, status='SCHEDULED').count()
    
    if active_students > 0 or active_lessons > 0:
        messages.error(
            request,
            f'Cannot archive branch with {active_students} active students and {active_lessons} active lessons'
        )
        return redirect('branch_detail', pk=branch.pk)
    
    branch.status = 'archived'
    branch.save()
    messages.success(request, f'Branch "{branch.name}" archived')
    return redirect('branch_list')
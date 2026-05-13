from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Subject
from branches.models import Branch


def check_admin(user):
    """Перевірити, чи користувач є адміністратором"""
    return user.is_authenticated and user.role == 'ADMIN'


@login_required(login_url='login')
def subject_list(request):
    """Список предметів"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branch_id = request.GET.get('branch')
    subjects = Subject.objects.filter(status='active')
    branches = Branch.objects.filter(status='active')
    
    if branch_id:
        subjects = subjects.filter(branch_id=branch_id)
    
    context = {
        'subjects': subjects,
        'branches': branches,
        'selected_branch': branch_id,
        'archived_count': Subject.objects.filter(status='archived').count(),
    }
    return render(request, 'subjects/subject_list.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def subject_create(request):
    """Створити новий предмет"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branches = Branch.objects.filter(status='active')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        branch_id = request.POST.get('branch')
        
        if not name or not branch_id:
            messages.error(request, 'Subject name and branch are required')
            return render(request, 'subjects/subject_form.html', {'branches': branches})
        
        branch = get_object_or_404(Branch, pk=branch_id, status='active')
        
        # Перевіримо унікальність
        if Subject.objects.filter(name=name, branch=branch).exists():
            messages.error(request, f'Subject "{name}" already exists in this branch')
            return render(request, 'subjects/subject_form.html', {'branches': branches})
        
        Subject.objects.create(
            name=name,
            branch=branch,
            status='active'
        )
        messages.success(request, f'Subject "{name}" created')
        return redirect('subject_list')
    
    context = {'branches': branches}
    return render(request, 'subjects/subject_form.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def subject_edit(request, pk):
    """Редагувати предмет"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    subject = get_object_or_404(Subject, pk=pk)
    branches = Branch.objects.filter(status='active')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            messages.error(request, 'Subject name is required')
            return render(request, 'subjects/subject_form.html', {
                'subject': subject,
                'branches': branches
            })
        
        subject.name = name
        subject.save()
        messages.success(request, 'Subject updated')
        return redirect('subject_list')
    
    context = {
        'subject': subject,
        'branches': branches,
        'is_edit': True,
    }
    return render(request, 'subjects/subject_form.html', context)


@login_required(login_url='login')
def subject_archive(request, pk):
    """Архівувати предмет"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    subject = get_object_or_404(Subject, pk=pk)
    subject.status = 'archived'
    subject.save()
    messages.success(request, f'Subject "{subject.name}" archived')
    return redirect('subject_list')


@login_required(login_url='login')
def subject_detail(request, pk):
    """Деталі предмету"""
    subject = get_object_or_404(Subject, pk=pk)
    
    context = {
        'subject': subject,
    }
    return render(request, 'subjects/subject_detail.html', context)

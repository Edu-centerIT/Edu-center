from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Group, GroupMembership
from branches.models import Branch
from students.models import Student


def check_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'


@login_required(login_url='login')
def group_list(request):
    """Список груп"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    groups = Group.objects.filter(status='active')
    branches = Branch.objects.filter(status='active')
    
    branch_id = request.GET.get('branch')
    if branch_id:
        groups = groups.filter(branch_id=branch_id)
    
    context = {
        'groups': groups,
        'branches': branches,
        'selected_branch': branch_id,
    }
    return render(request, 'groups/group_list.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def group_create(request):
    """Створити нову групу"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branches = Branch.objects.filter(status='active')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        branch_id = request.POST.get('branch')
        
        if not name or not branch_id:
            messages.error(request, 'Group name and branch are required')
            return render(request, 'groups/group_form.html', {'branches': branches})
        
        branch = get_object_or_404(Branch, pk=branch_id, status='active')
        
        group = Group.objects.create(
            name=name,
            branch=branch,
            status='active'
        )
        messages.success(request, f'Group "{group.name}" created')
        return redirect('group_detail', pk=group.pk)
    
    context = {'branches': branches}
    return render(request, 'groups/group_form.html', context)


@login_required(login_url='login')
def group_detail(request, pk):
    """Деталі групи"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    group = get_object_or_404(Group, pk=pk)
    
    # Поточні члени групи
    memberships = GroupMembership.objects.filter(group=group, left_at__isnull=True)
    students_in_group = [m.student for m in memberships]
    
    # Доступні студенти для додавання
    available_students = Student.objects.filter(
        branch=group.branch,
        status='active'
    ).exclude(id__in=students_in_group)
    
    context = {
        'group': group,
        'members': memberships,
        'available_students': available_students,
    }
    return render(request, 'groups/group_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def group_edit(request, pk):
    """Редагувати групу"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    group = get_object_or_404(Group, pk=pk)
    branches = Branch.objects.filter(status='active')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            messages.error(request, 'Group name is required')
            return render(request, 'groups/group_form.html', {
                'group': group,
                'branches': branches,
                'is_edit': True,
            })
        
        group.name = name
        group.save()
        messages.success(request, 'Group updated')
        return redirect('group_detail', pk=group.pk)
    
    context = {
        'group': group,
        'branches': branches,
        'is_edit': True,
    }
    return render(request, 'groups/group_form.html', context)


@login_required(login_url='login')
def add_student_to_group(request, pk):
    """Додати студента до групи"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, pk=student_id, branch=group.branch, status='active')
        
        # Перевіримо, чи вже в групі
        if GroupMembership.objects.filter(group=group, student=student, left_at__isnull=True).exists():
            messages.warning(request, f'"{student.first_name}" is already in this group')
        else:
            GroupMembership.objects.create(group=group, student=student)
            messages.success(request, f'"{student.first_name}" added to group')
    
    return redirect('group_detail', pk=group.pk)


@login_required(login_url='login')
def remove_student_from_group(request, pk, student_id):
    """Видалити студента з групи"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    group = get_object_or_404(Group, pk=pk)
    membership = get_object_or_404(GroupMembership, group=group, student_id=student_id, left_at__isnull=True)
    
    student_name = membership.student.first_name
    from django.utils import timezone
    membership.left_at = timezone.now()
    membership.save()
    
    messages.success(request, f'"{student_name}" removed from group')
    return redirect('group_detail', pk=group.pk)
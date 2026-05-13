from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Student, Parent
from branches.models import Branch
from attendance.models import Attendance


def check_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'


@login_required(login_url='login')
def student_list(request):
    """Список студентів"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    students = Student.objects.filter(status='active')
    
    # Фільтрація
    branch_id = request.GET.get('branch') #url
    search = request.GET.get('search', '').strip() # url name , прибирає пробіли
    
    if branch_id:
        students = students.filter(branch_id=branch_id)
    
    if search:
        students = students.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)
        )
    
    branches = Branch.objects.filter(status='active')
    archived_count = Student.objects.filter(status='archived').count()
    
    context = {
        'students': students,
        'branches': branches,
        'archived_count': archived_count,
        'selected_branch': branch_id,
        'search_query': search,
    }
    return render(request, 'students/student_list.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def student_create(request):
    """Створити нового студента"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    branches = Branch.objects.filter(status='active')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip() #прибирає пробіли
        last_name = request.POST.get('last_name', '').strip()#request.POST html forms
        date_of_birth = request.POST.get('date_of_birth')
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        branch_id = request.POST.get('branch')
        
        # Parent info
        parent_name = request.POST.get('parent_name', '').strip()
        parent_phone = request.POST.get('parent_phone', '').strip()
        parent_email = request.POST.get('parent_email', '').strip()
        parent_relationship = request.POST.get('parent_relationship', '').strip()
        
        if not first_name or not last_name or not branch_id: # Валідація
            messages.error(request, 'Name and branch are required')
            return render(request, 'students/student_form.html', {'branches': branches})
        
        branch = get_object_or_404(Branch, pk=branch_id, status='active')
        
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth or None,
            phone=phone,
            email=email,
            address=address,
            branch=branch,
            status='active'
        )
        
        if parent_name and parent_phone:
            Parent.objects.create(
                student=student,
                name=parent_name,
                phone=parent_phone,
                email=parent_email,
                relationship=parent_relationship
            )
        
        messages.success(request, f'Student "{student.first_name} {student.last_name}" created')
        return redirect('student_detail', pk=student.pk)
    
    context = {'branches': branches}
    return render(request, 'students/student_form.html', context)


@login_required(login_url='login')
def student_detail(request, pk):
    """Деталі студента"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, pk=pk)
    parent = Parent.objects.filter(student=student).first()
    
    # Історія відвідування
    attendance_records = Attendance.objects.filter(student=student).select_related('lesson').order_by('-recorded_at') #одразу підтягує lesson   order_by('-recorded_at сортує: нові → зверху старі → знизу
    attended = attendance_records.filter(is_present=True).count() #скільки разів був
    missed = attendance_records.filter(is_present=False).count() #скільки пропустив
    
    context = {
        'student': student,
        'parent': parent,
        'attendance_records': attendance_records[:10],
        'attended': attended,
        'missed': missed,
    }
    return render(request, 'students/student_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def student_edit(request, pk):
    """Редагувати студента"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, pk=pk)
    parent = Parent.objects.filter(student=student).first()
    branches = Branch.objects.filter(status='active')
    
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name', '').strip()
        student.last_name = request.POST.get('last_name', '').strip()
        student.date_of_birth = request.POST.get('date_of_birth') or None
        student.phone = request.POST.get('phone', '').strip()
        student.email = request.POST.get('email', '').strip()
        student.address = request.POST.get('address', '').strip()
        
        if not student.first_name or not student.last_name:
            messages.error(request, 'Name fields are required')
            return render(request, 'students/student_form.html', {
                'student': student, # об’єднує: HTML-шаблон (student_form.html) i дані (context)
                'parent': parent,
                'branches': branches
            })
        
        student.save()
        
        # Update parent info
        parent_name = request.POST.get('parent_name', '').strip()
        parent_phone = request.POST.get('parent_phone', '').strip()
        
        if parent_name and parent_phone:
            if parent:
                parent.name = parent_name
                parent.phone = parent_phone
                parent.email = request.POST.get('parent_email', '').strip()
                parent.relationship = request.POST.get('parent_relationship', '').strip()
                parent.save()
            else:
                Parent.objects.create(
                    student=student,
                    name=parent_name,
                    phone=parent_phone,
                    email=request.POST.get('parent_email', '').strip(),
                    relationship=request.POST.get('parent_relationship', '').strip()
                )
        
        messages.success(request, 'Student updated successfully')
        return redirect('student_detail', pk=student.pk)
    
    context = {
        'student': student,
        'parent': parent,
        'branches': branches,
        'is_edit': True,
    }
    return render(request, 'students/student_form.html', context)


@login_required(login_url='login')
def student_archive(request, pk):
    """Архівувати студента"""
    if not check_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, pk=pk)
    student.status = 'archived'
    student.save()
    messages.success(request, f'Student "{student.first_name}" archived')
    return redirect('student_list')
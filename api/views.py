from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from users.models import CustomUser
from branches.models import Branch
from subjects.models import Subject
from students.models import Student
from groups.models import Group
from lessons.models import Lesson
from attendance.models import Attendance

from .serializers import (
    CustomUserSerializer, BranchSerializer, SubjectSerializer,
    StudentSerializer, GroupSerializer, LessonSerializer, AttendanceSerializer
)


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API для управління користувачами.
    
    list: Отримати список всіх користувачів
    create: Створити нового користувача
    retrieve: Отримати деталі користувача
    update: Оновити користувача
    destroy: Видалити користувача
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def teachers(self, request):
        """Отримати список вчителів"""
        teachers = CustomUser.objects.filter(role='TEACHER', is_active=True)
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def admins(self, request):
        """Отримати список адміністраторів"""
        admins = CustomUser.objects.filter(role='ADMIN', is_active=True)
        serializer = self.get_serializer(admins, many=True)
        return Response(serializer.data)


class BranchViewSet(viewsets.ModelViewSet):
    """
    API для управління філіями.
    
    list: Отримати список всіх філій
    create: Створити нову філію
    retrieve: Отримати деталі філії
    update: Оновити філію
    destroy: Видалити філію
    """
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Branch.objects.all()
    
    @action(detail=False, methods=['get'])
    def archived(self, request):
        """Отримати архівовані філії"""
        archived_branches = Branch.objects.filter(status='archived')
        serializer = self.get_serializer(archived_branches, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API для управління предметами.
    
    list: Отримати список всіх предметів
    create: Створити новий предмет
    retrieve: Отримати деталі предмета
    update: Оновити предмет
    destroy: Видалити предмет
    """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        branch = self.request.query_params.get('branch')
        queryset = Subject.objects.filter(status='active')
        if branch:
            queryset = queryset.filter(branch_id=branch)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_branch(self, request):
        """Отримати предмети за філією"""
        branch_id = request.query_params.get('branch_id')
        if not branch_id:
            return Response({'error': 'branch_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        subjects = Subject.objects.filter(branch_id=branch_id, status='active')
        serializer = self.get_serializer(subjects, many=True)
        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    """
    API для управління студентами.
    
    list: Отримати список всіх студентів
    create: Створити нового студента
    retrieve: Отримати деталі студента
    update: Оновити студента
    destroy: Видалити студента
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        branch = self.request.query_params.get('branch')
        queryset = Student.objects.filter(status='active')
        if branch:
            queryset = queryset.filter(branch_id=branch)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_branch(self, request):
        """Отримати студентів за філією"""
        branch_id = request.query_params.get('branch_id')
        if not branch_id:
            return Response({'error': 'branch_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        students = Student.objects.filter(branch_id=branch_id, status='active')
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API для управління групами.
    
    list: Отримати список всіх груп
    create: Створити нову групу
    retrieve: Отримати деталі групи
    update: Оновити групу
    destroy: Видалити групу
    """
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        branch = self.request.query_params.get('branch')
        queryset = Group.objects.filter(status='active')
        if branch:
            queryset = queryset.filter(branch_id=branch)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_branch(self, request):
        """Отримати групи за філією"""
        branch_id = request.query_params.get('branch_id')
        if not branch_id:
            return Response({'error': 'branch_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        groups = Group.objects.filter(branch_id=branch_id, status='active')
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """
    API для управління уроками.
    
    list: Отримати список всіх уроків
    create: Створити новий урок
    retrieve: Отримати деталі уроку
    update: Оновити урок
    destroy: Видалити урок
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Lesson.objects.filter(status='SCHEDULED')
    
    @action(detail=False, methods=['get'])
    def my_schedule(self, request):
        """Отримати мій розклад (для вчителя)"""
        if request.user.role != 'TEACHER':
            return Response({'error': 'Only teachers can access this'}, status=status.HTTP_403_FORBIDDEN)
        
        lessons = Lesson.objects.filter(teacher=request.user, status='SCHEDULED').order_by('date', 'start_time')
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """Отримати уроки на конкретну дату"""
        date = request.query_params.get('date')
        if not date:
            return Response({'error': 'date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        lessons = Lesson.objects.filter(date=date, status='SCHEDULED')
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_branch(self, request):
        """Отримати уроки за філією"""
        branch_id = request.query_params.get('branch_id')
        if not branch_id:
            return Response({'error': 'branch_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        lessons = Lesson.objects.filter(branch_id=branch_id, status='SCHEDULED')
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API для управління відвідуванням.
    
    list: Отримати список всіх записів про відвідування
    create: Створити новий запис про відвідування
    retrieve: Отримати деталі запису про відвідування
    update: Оновити запис про відвідування
    destroy: Видалити запис про відвідування
    """
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Attendance.objects.all()
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Отримати відвідування студента"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance = Attendance.objects.filter(student_id=student_id)
        serializer = self.get_serializer(attendance, many=True)
        
        # Обчислити статистику
        total = attendance.count()
        present = attendance.filter(is_present=True).count()
        percentage = (present / total * 100) if total > 0 else 0
        
        return Response({
            'data': serializer.data,
            'statistics': {
                'total': total,
                'present': present,
                'absent': total - present,
                'percentage': round(percentage, 2)
            }
        })
    
    @action(detail=False, methods=['get'])
    def by_lesson(self, request):
        """Отримати відвідування на конкретний урок"""
        lesson_id = request.query_params.get('lesson_id')
        if not lesson_id:
            return Response({'error': 'lesson_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance = Attendance.objects.filter(lesson_id=lesson_id)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)
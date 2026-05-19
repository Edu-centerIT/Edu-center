from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet,
    BranchViewSet,
    SubjectViewSet,
    StudentViewSet,
    GroupViewSet,
    LessonViewSet,
    AttendanceViewSet, 
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'branches', BranchViewSet, basename='branches')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),

   
    path('subscriptions/', include('subscriptions.urls')),

]
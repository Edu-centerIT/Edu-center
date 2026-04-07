from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.lesson_list, name='lesson_list'),
    path('create/', views.lesson_create, name='lesson_create'),
    path('<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('<int:pk>/cancel/', views.lesson_cancel, name='lesson_cancel'),
]
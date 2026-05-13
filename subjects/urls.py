from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.subject_list, name='subject_list'),
    path('create/', views.subject_create, name='subject_create'),
    path('<int:pk>/edit/', views.subject_edit, name='subject_edit'), 
    path('<int:pk>/archive/', views.subject_archive, name='subject_archive'),
]
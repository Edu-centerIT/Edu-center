from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.group_list, name='group_list'),
    path('create/', views.group_create, name='group_create'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('<int:pk>/add-student/', views.add_student_to_group, name='add_student_to_group'),
    path('<int:pk>/remove-student/<int:student_id>/', views.remove_student_from_group, name='remove_student_from_group'),
] 
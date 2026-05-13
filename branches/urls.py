from django.urls import path
from . import views 

urlpatterns = [
    path('list/', views.branch_list, name='branch_list'),
    path('create/', views.branch_create, name='branch_create'),
    path('<int:pk>/', views.branch_detail, name='branch_detail'),
    path('<int:pk>/edit/', views.branch_edit, name='branch_edit'),
    path('<int:pk>/archive/', views.branch_archive, name='branch_archive'),
]
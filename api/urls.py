from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from api.views import (
    CustomUserViewSet, BranchViewSet, SubjectViewSet,
    StudentViewSet, GroupViewSet, LessonViewSet, AttendanceViewSet
)
from subscriptions.views import (
    SubscriptionPlanViewSet, PricingTierViewSet, StudentSubscriptionViewSet
)

#Це карта маршрутів вашого API

router = DefaultRouter()

#  Користувачі, Філії, Предмети, тощо
router.register(r'users', CustomUserViewSet, basename='user') #автоматичний генератор маршрутів для REST API.
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

#  НОВЕ: Subscription через Router!
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'pricing-tiers', PricingTierViewSet, basename='pricing-tier')
router.register(r'student-subscriptions', StudentSubscriptionViewSet, basename='student-subscription')

urlpatterns = [
    path('', include(router.urls)),
]
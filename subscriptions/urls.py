from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionPlanViewSet,
    PricingTierViewSet,
    StudentSubscriptionViewSet
)

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='plan')
router.register(r'tiers', PricingTierViewSet, basename='tier')
router.register(r'student-subscriptions', StudentSubscriptionViewSet, basename='student-subscription')

urlpatterns = [
    path('', include(router.urls)),
]
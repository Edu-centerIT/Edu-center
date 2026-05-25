from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SubscriptionPlan, PricingTier, StudentSubscription
from api.serializers import (
    SubscriptionPlanSerializer,
    PricingTierSerializer,
    StudentSubscriptionSerializer
)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    API для управління планами підписок.
    
    list: Отримати список всіх планів
    create: Створити новий план
    retrieve: Отримати деталі плану
    update: Оновити план
    destroy: Видалити план
    """
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return SubscriptionPlan.objects.all()
        return SubscriptionPlan.objects.none()
    
    @action(detail=False, methods=['get'])
    def by_branch(self, request):
        """Отримати плани за філією"""
        branch_id = request.query_params.get('branch_id')
        if not branch_id:
            return Response(
                {'error': 'branch_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plans = SubscriptionPlan.objects.filter(
            branch_id=branch_id,
            status='active'
        )
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)


class PricingTierViewSet(viewsets.ModelViewSet):
    """
    API для управління цінами.
    
    list: Отримати список всіх цін
    create: Створити нову ціну
    retrieve: Отримати деталі ціни
    update: Оновити ціну
    destroy: Видалити ціну
    """
    serializer_class = PricingTierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return PricingTier.objects.all()
        return PricingTier.objects.none()
    
    @action(detail=False, methods=['get'])
    def by_plan(self, request):
        """Отримати ціни плану"""
        plan_id = request.query_params.get('plan_id')
        if not plan_id:
            return Response(
                {'error': 'plan_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tiers = PricingTier.objects.filter(plan_id=plan_id)
        serializer = self.get_serializer(tiers, many=True)
        return Response(serializer.data)


class StudentSubscriptionViewSet(viewsets.ModelViewSet):
    """
    API для управління підписками студентів.
    
    list: Отримати список всіх підписок
    create: Створити нову підписку
    retrieve: Отримати деталі підписки
    update: Оновити підписку
    destroy: Видалити підписку
    """
    serializer_class = StudentSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return StudentSubscription.objects.all()
        return StudentSubscription.objects.none()
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Отримати підписки студента"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscriptions = StudentSubscription.objects.filter(student_id=student_id)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(subscriptions)
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """Отримати підписки на предмет"""
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response(
                {'error': 'subject_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscriptions = StudentSubscription.objects.filter(subject_id=subject_id)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)
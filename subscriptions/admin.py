from django.contrib import admin
from .models import SubscriptionPlan, PricingTier, StudentSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'plan_type', 'status', 'created_at']
    list_filter = ['branch', 'plan_type', 'status']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    #  ВИДАЛИЛИ total_cost (обчислюється в методі)
    list_display = ['plan', 'lessons_per_month', 'price_per_lesson', 'get_total_cost']
    list_filter = ['plan']
    
    def get_total_cost(self, obj):
        """Обчислити загальну вартість"""
        return obj.lessons_per_month * obj.price_per_lesson
    get_total_cost.short_description = 'Total Cost'


@admin.register(StudentSubscription)
class StudentSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['student', 'plan', 'subject', 'start_date', 'created_at']
    list_filter = ['plan', 'subject', 'start_date']
    search_fields = ['student__first_name', 'student__last_name']
    readonly_fields = ['created_at']
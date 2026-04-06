from django.db import models
from branches.models import Branch ,Subject, Student


# Create your models here.
class SubscriptionPlan(models.Model):
    PLAN_TYPE_CHOICES = [('individual', 'Individual'), ('group', 'Group')]
    
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES)
    subjects = models.ManyToManyField(Subject)
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class PricingTier(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='tiers')
    lessons_per_month = models.IntegerField()
    price_per_lesson = models.DecimalField(max_digits=10, decimal_places=2)

class StudentSubscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
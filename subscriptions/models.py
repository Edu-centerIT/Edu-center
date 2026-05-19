

from django.db import models
from branches.models import Branch
from subjects.models import Subject
from students.models import Student


class SubscriptionPlan(models.Model):
    """План підписки з цінами"""
    
    PLAN_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES)
    subjects = models.ManyToManyField(Subject)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subscriptions_subscriptionplan'
        unique_together = ['name', 'branch']
    
    def __str__(self):
        return f"{self.name} ({self.branch.name})"


class PricingTier(models.Model):
    """Цінові рівні плану"""
    
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    lessons_per_month = models.IntegerField()
    price_per_lesson = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'subscriptions_pricingtier'
        unique_together = ['plan', 'lessons_per_month']
        ordering = ['lessons_per_month']
    
    def __str__(self):
        return f"{self.plan.name} - {self.lessons_per_month} lessons: ${self.price_per_lesson}"


class StudentSubscription(models.Model):
    """Підписка студента на план"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subscriptions_studentsubscription'
        unique_together = ['student', 'plan', 'subject']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.plan.name} ({self.subject.name})"
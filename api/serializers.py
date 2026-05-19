from rest_framework import serializers
from users.models import CustomUser
from branches.models import Branch
from subjects.models import Subject
from students.models import Student, Parent
from groups.models import Group, GroupMembership
from lessons.models import Lesson
from attendance.models import Attendance


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer для користувачів"""
    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
        read_only_fields = ['id']


class BranchSerializer(serializers.ModelSerializer):
    """Serializer для філій"""
    class Meta:
        model = Branch
        fields = ['id', 'name', 'city', 'address', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer для предметів"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'branch', 'branch_name', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class ParentSerializer(serializers.ModelSerializer):
    """Serializer для батьків"""
    class Meta:
        model = Parent
        fields = ['id', 'student', 'name', 'phone', 'email', 'relationship']
        read_only_fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    """Serializer для студентів"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    parent = ParentSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'date_of_birth', 
                  'branch', 'branch_name', 'status', 'parent', 'created_at']
        read_only_fields = ['id', 'created_at']


class GroupMembershipSerializer(serializers.ModelSerializer):
    """Serializer для членства в групах"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = GroupMembership
        fields = ['id', 'group', 'student', 'student_name', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class GroupSerializer(serializers.ModelSerializer):
    """Serializer для груп"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'branch', 'branch_name', 'status', 'members_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_members_count(self, obj):
        return obj.students.count()


class LessonSerializer(serializers.ModelSerializer):
    """Serializer для уроків"""
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True, allow_null=True)
    group_name = serializers.CharField(source='group.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name', 'branch', 'branch_name',
                  'lesson_type', 'student', 'student_name', 'group', 'group_name', 'date', 
                  'start_time', 'end_time', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer для відвідування"""
    lesson_info = LessonSerializer(source='lesson', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'lesson', 'lesson_info', 'student', 'student_name', 'is_present', 'notes']
        read_only_fields = ['id']




from rest_framework import serializers
from .models import SubscriptionPlan, PricingTier, StudentSubscription


class PricingTierSerializer(serializers.ModelSerializer):
    """Serializer для цінових рівнів"""
    total_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = PricingTier
        fields = ['id', 'plan', 'lessons_per_month', 'price_per_lesson', 'total_cost']
        read_only_fields = ['id']
    
    def get_total_cost(self, obj):
        return obj.lessons_per_month * obj.price_per_lesson


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer для планів підписок"""
    pricing_tiers = PricingTierSerializer(
        source='pricingtier_set',
        many=True,
        read_only=True
    )
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    subjects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'branch', 'branch_name', 'plan_type',
            'status', 'pricing_tiers', 'subjects_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_subjects_count(self, obj):
        return obj.subjects.count()








class StudentSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer для підписок студентів"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    pricing_info = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentSubscription
        fields = [
            'id', 'student', 'student_name', 'plan', 'plan_name',
            'subject', 'subject_name', 'start_date', 'pricing_info', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_pricing_info(self, obj):
        """Отримати інформацію про ціни плану"""
        tiers = obj.plan.pricingtier_set.all()
        return PricingTierSerializer(tiers, many=True).data
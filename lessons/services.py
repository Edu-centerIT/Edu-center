from .models import Lesson


def check_teacher_conflict(teacher, date, start_time, end_time, exclude_lesson=None):
    """
    Перевірити конфлікт розкладу вчителя
    
    Returns: (is_valid, error_message)
    """
    lessons = Lesson.objects.filter(
        teacher=teacher,
        date=date,
        status__in=['SCHEDULED', 'COMPLETED']
    )
    
    if exclude_lesson:
        lessons = lessons.exclude(id=exclude_lesson.id)
    
    for lesson in lessons:
        # Конфлікт: start1 < end2 AND start2 < end1
        if lesson.start_time < end_time and start_time < lesson.end_time:
            return False, f"Teacher has conflict with lesson at {lesson.start_time}-{lesson.end_time}"
    
    return True, None


def check_student_conflict(student, date, start_time, end_time, exclude_lesson=None):
    """
    Перевірити конфлікт розкладу студента
    
    Returns: (is_valid, error_message)
    """
    lessons = Lesson.objects.filter(
        student=student,
        date=date,
        status__in=['SCHEDULED', 'COMPLETED']
    )
    
    if exclude_lesson:
        lessons = lessons.exclude(id=exclude_lesson.id)
    
    for lesson in lessons:
        if lesson.start_time < end_time and start_time < lesson.end_time:
            return False, f"Student has conflict with lesson at {lesson.start_time}-{lesson.end_time}"
    
    return True, None


def check_group_conflicts(group, date, start_time, end_time):
    """
    Перевірити конфлікти для всіх членів групи
    
    Returns: (is_valid, error_message)
    """
    from groups.models import GroupMembership
    
    # Отримуємо поточних членів групи
    memberships = GroupMembership.objects.filter(group=group, left_at__isnull=True)
    
    for membership in memberships:
        is_valid, error = check_student_conflict(membership.student, date, start_time, end_time)
        if not is_valid:
            return False, f"{membership.student.first_name}: {error}"
    
    return True, None
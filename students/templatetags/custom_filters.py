from django import template

from students.models import Attendance

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Dictionarydan key bo'yicha qiymat olish"""
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None


@register.filter
def get_attendance(dictionary, student_date_tuple):
    """Get attendance status from dictionary using student_id and date as a tuple"""
    if hasattr(dictionary, 'get'):
        student_id, date = student_date_tuple
        return dictionary.get((student_id, date))
    return None


@register.filter
def concat(value, arg):
    """Create a tuple from two values"""
    return (value, arg)


@register.filter
def is_column_present(date, group_id):
    """Check if all students are present for this date"""
    from django.db.models import Count

    date_str = date.strftime('%Y-%m-%d')
    present_count = Attendance.objects.filter(
        group_id=group_id,
        date=date_str,
        status='present'
    ).count()

    absent_count = Attendance.objects.filter(
        group_id=group_id,
        date=date_str,
        status='absent'
    ).count()

    # Consider the column "present" if more than half are present
    return present_count >= absent_count

from collections import defaultdict
from django.db.models import Count, Q, Prefetch
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
from students.models import Group, Attendance, Student


def dashboard(request):
    return render(request, 'dashboard_components.html')


def employee(request):
    return render(request, 'employee.html')


def groups(request):
    groups = Group.objects.annotate(
        active_st_count=Count('students', filter=Q(students__status='active')),
        students_total_count=Count('students')
    )
    for group in groups:
        group.active_ratio = (
            round(group.active_st_count / group.students_total_count * 100, 1)
            if group.students_total_count > 0 else 0
        )

    context = {
        "groups": groups,
    }
    return render(request, 'dash_group.html', context=context)


def events(request):
    return render(request, 'dash_event.html')


def group_attendance(request, group_id):
    group = get_object_or_404(
        Group.objects.prefetch_related(
            Prefetch('students', queryset=Student.objects.filter(status='active'))
        ),
        id=group_id
    )

    # Get current month dates
    today = timezone.now().date()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    dates = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]

    # Get attendance data
    attendances = Attendance.objects.filter(
        group=group,
        date__range=(first_day, last_day)
    ).select_related('student')

    # Create attendance map
    attendance_map = {
        (att.student_id, att.date): att.status
        for att in attendances
    }

    context = {
        'group': group,
        'dates': dates,
        'students': group.students.filter(status='active'),
        'attendance_map': attendance_map,
    }
    return render(request, 'group_attendance.html', context)


@require_POST
def update_attendance(request, group_id, student_id, date):
    group = get_object_or_404(Group, id=group_id)
    student = get_object_or_404(Student, id=student_id)
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    attendance, created = Attendance.objects.get_or_create(
        group=group,
        student=student,
        date=date_obj,
        defaults={'status': Attendance.PRESENT}
    )

    if not created:
        attendance.status = (
            Attendance.ABSENT if attendance.status == Attendance.PRESENT
            else Attendance.PRESENT
        )
        attendance.save()

    context = {
        'group_id': group.id,
        'student_id': student.id,
        'date': date,
        'status': attendance.status,
    }
    return render(request, 'attendance_cell.html', context)


@require_POST
def toggle_column(request, group_id, date):
    group = get_object_or_404(Group, id=group_id)
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    # Get current state of the column
    present_count = Attendance.objects.filter(
        group=group,
        date=date_obj,
        status='present'
    ).count()

    # Determine new status (toggle all)
    new_status = 'absent' if present_count > 0 else 'present'

    # Update all attendance records
    students = group.students.filter(status='active')
    for student in students:
        Attendance.objects.update_or_create(
            group=group,
            student=student,
            date=date_obj,
            defaults={'status': new_status}
        )

    # Return the updated table
    return group_attendance(request, group_id)

from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

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


def group_detail(request, pk):
    group = get_object_or_404(Group, id=pk)
    context = {
        "group": group,
        "dates": range(1, 30, 2),
        "students": group.students.all()
    }
    return render(request, 'group_detail.html', context=context)


def events(request):
    return render(request, 'dash_event.html')


@require_POST
def update_attendance(request, group_id, student_id, date):
    group = get_object_or_404(Group, id=group_id)
    student = get_object_or_404(Student, id=student_id)

    # Get current status
    attendance, created = Attendance.objects.get_or_create(
        group=group,
        student=student,
        date=date,
        defaults={'status': ''}
    )

    # Cycle through statuses
    if attendance.status == '':
        attendance.status = 'present'
    elif attendance.status == 'present':
        attendance.status = 'absent'
    else:
        attendance.status = ''

    attendance.save()

    # Return updated cell
    context = {
        'attendance': attendance.status,
        'date': date,
        'student': student,
    }
    html = render_to_string('group_detail.html', context)
    return HttpResponse(html)


@require_POST
def toggle_column(request, group_id, date):
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()

    # Determine new status (toggle all empty/present)
    has_present = Attendance.objects.filter(
        group=group,
        date=date,
        status='present'
    ).exists()

    new_status = 'present' if not has_present else ''

    # Update all students in this group/date
    for student in students:
        attendance, created = Attendance.objects.get_or_create(
            group=group,
            student=student,
            date=date,
            defaults={'status': new_status}
        )
        if not created:
            attendance.status = new_status
            attendance.save()

    # Return full table
    context = {
        'group': group,
        'dates': group.get_attendance_dates(),  # Implement this method
        'students': students,
    }
    html = render_to_string('group_detail.html', context)
    return HttpResponse(html)

from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404

from students.models import Group


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
        "dates": range(1, 30, 2)
    }
    return render(request, 'group_detail.html', context=context)


def events(request):
    return render(request, 'dash_event.html')

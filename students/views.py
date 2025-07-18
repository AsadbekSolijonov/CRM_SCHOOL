from django.shortcuts import render


def dashboard(request):
    return render(request, 'dashboard_components.html')


def employee(request):
    return render(request, 'employee.html')


def groups(request):
    return render(request, 'dash_group.html')


def events(request):
    return render(request, 'dash_event.html')
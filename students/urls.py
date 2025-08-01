from django.urls import path
from students import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employee/', views.employee, name='employee'),
    path('groups/', views.groups, name='groups'),
    path('events/', views.events, name='events'),
    path('groups/<int:group_id>/', views.group_attendance, name='group_attendance'),

    path('groups/<int:group_id>/attendance/', views.group_attendance, name='group_attendance'),
    path('attendance/<int:group_id>/<int:student_id>/<str:date>/update/',\
         views.update_attendance, name='update_attendance'),
    path('attendance/<int:group_id>/<str:date>/toggle/',
         views.toggle_column, name='toggle_column'),
]

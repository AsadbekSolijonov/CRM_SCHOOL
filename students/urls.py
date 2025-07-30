from django.urls import path
from students import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employee/', views.employee, name='employee'),
    path('groups/', views.groups, name='groups'),
    path('group_detail/<int:pk>/', views.group_detail, name='group_detail'),
    path('events/', views.events, name='events'),
    path('group/<int:group_id>/attendance/<int:student_id>/<str:date>/',
         views.update_attendance, name='update_attendance'),
    path('group/<int:group_id>/toggle_column/<str:date>/',
         views.toggle_column, name='toggle_column'),
]

from django.urls import path
from students import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employee/', views.employee, name='employee'),
    path('groups/', views.groups, name='groups'),
    path('group_detail/<int:pk>/', views.group_detail, name='group_detail'),
    path('events/', views.events, name='events')
]

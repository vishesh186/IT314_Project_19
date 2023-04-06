"""ProjectManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ProjectManagementSystemApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'),
    path('landing/', views.Landing, name='Landing'),
    path('login/', views.Login, name='Login'),

    path('view-projects/', views.ViewProjects, name='ViewProjects'),
    path('project-dashboard/', views.ProjectDashboard, name='ProjectDashboard'),
    path('view-teams/', views.ViewTeams, name='ViewTeams'),
    path('team-dashboard/', views.TeamDashboard, name='TeamDashboard'),

    path('create-project/', views.CreateProject, name='CreateProject'),
    path('create-team/', views.CreateTeam, name='CreateTeam'),
    path('create-task/', views.CreateTask, name='CreateTask'),
    path('submit-report/', views.SubmitReport, name='SubmitReport'),
    
    path('resources/', views.Resources, name='Resources'),
    path('manage-resources/', views.ManageResources, name='ManageResources'),
    path('resource-booking-request/', views.RequestResource, name='RequestResource'),
]
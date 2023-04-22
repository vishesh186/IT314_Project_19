from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.forms.models import model_to_dict
from django.core.exceptions import PermissionDenied
from datetime import datetime

# Create your views here.

def Home(request):
    return render(request, 'home.html')


def Landing(request):
    return render(request, 'landing.html')


def Login(request):
    return render(request, 'login.html')


def CreateProject(request):
    # projectManagers = Employee.objects.filter(role='PM')
    teams = Team.objects.all()
    if request.method == "POST":
        timestamp = datetime.now()
        project = Project(
            projectID="PRJ"+timestamp.strftime("%d%m%y%H%M%S"),
            title=request.POST['title'],
            client=request.POST['client'],
            description=request.POST['description'],
            budget=request.POST['budget'],
            deadline=request.POST['deadline'],
            team=model_to_dict(teams.get(teamID=request.POST['team']))  
        )
        project.save()
        return redirect('ViewProjects')
    return render(request, 'createProject.html', {'teams':teams})


def ViewProjects(request):
    # projectManager = Employee.objects.filter(employeeID=request.user.username, role='PM')
    # if projectManager:
    #     projectManager = projectManager[0]
    # else:
    #     raise PermissionDenied
   
    # projects = Project.objects.filter(team__managerID=projectManager.employeeID)
    projects = Project.objects.all()
    return render(request, 'viewProjects.html', {'projects':projects})


def ProjectDashboard(request, projectID):
    project = Project.objects.get(projectID=projectID)
    teamMembers = Employee.objects.filter(team=project.team)
    inprogressTasks = Task.objects.filter(projectID=projectID, status='I')
    completedTasks = Task.objects.filter(projectID=projectID, status='C')
    submittedForReviewTasks = Task.objects.filter(projectID=projectID, status='R')
    return render(request, 'projectDashboard.html', {'project':project, 'teamMembers':teamMembers, 
                    'inprogress': inprogressTasks,
                    'completed':completedTasks,
                    'review':submittedForReviewTasks})


def CreateTeam(request):
    return render(request, 'createTeam.html')


def CreateTask(request, projectID):
    project = Project.objects.get(projectID=projectID)
    if request.method == "POST":
        timestamp = datetime.now()
        assignee = request.POST['assignee'].split('-')
        print(assignee)
        task = Task(
            taskID="TSK"+timestamp.strftime("%d%m%y%H%M%S"),
            title=request.POST['title'],
            allocatedBudget=request.POST['budget'],
            description=request.POST['description'],
            employeeID=assignee[1],
            employeeName=assignee[0],
            deadline=request.POST['deadline'],
            assigned=timestamp,
            projectID=projectID,
            managerID=project.team['managerID'],
            status='I'
        )
        task.save()
    return redirect(reverse("ProjectDashboard", kwargs={"projectID": projectID}))


def SubmitReport(request):
    return render(request, 'submitReport.html')


def ViewTeams(request):
    return render(request, 'viewTeams.html')


def TeamDashboard(request):
    return render(request, 'teamDashboard.html')


def Resources(request):
    return render(request, 'viewResources.html')


def RequestResource(request):
    if request.method == "POST":
        timestamp = datetime.now()
        resources = Resources(
            resourceID = "RSC" + timestamp.strftime("%d%m%y%H%M%S"),
            slot = request.POST['slot'],
            purpose = request.POST['purpose'],
        )
        resources.save()
        return redirect('ViewResources')
    return render(request, 'requestResource.html')


def ManageResources(request):
    return render(request, 'manageResources.html')

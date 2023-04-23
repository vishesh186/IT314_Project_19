from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# Create your views here.

def Home(request):
    return render(request, 'home.html')


def Landing(request):
    return render(request, 'landing.html')


def Login(request):
    return render(request, 'login.html')


# Only for Admin/Owner
def CreateProject(request):
    # projectManagers = Employee.objects.filter(role='PM')
    teams = Team.objects.all()
    if request.method == "POST":
        timestamp = datetime.now()
        team = teams.get(teamID=request.POST['team'])
        project = Project(
            projectID="PRJ"+timestamp.strftime("%d%m%y%H%M%S"),
            title=request.POST['title'],
            client=request.POST['client'],
            description=request.POST['description'],
            allocatedBudget=request.POST['budget'],
            deadline=request.POST['deadline'],
            teamID=team.teamID,
            teamName=team.name,
            managerID=team.managerID,
            managerName=team.managerName,
            status='O'
        )
        project.save()
        return redirect('ViewProjects')
    return render(request, 'createProject.html', {'teams':teams})


# As per employee type. PM, RM, E(Team-wise), Owner (All)  
def ViewProjects(request):
    ongoingProjects = Project.objects.filter(status='O')
    completedProjects = Project.objects.filter(status='C')
    return render(request, 'viewProjects.html', {'ongoingProjects':ongoingProjects, 'completedProjects':completedProjects})


def ProjectDashboard(request, projectID):
    project = Project.objects.get(projectID=projectID)
    teamMembers = Employee.objects.filter(teamID=project.teamID)
    inprogressTasks = Task.objects.filter(projectID=projectID, status='I')
    completedTasks = Task.objects.filter(projectID=projectID, status='C')
    submittedForReviewTasks = Task.objects.filter(projectID=projectID, status='R')
    return render(request, 'projectDashboard.html', {'project':project, 'teamMembers':teamMembers, 
                    'inprogress': inprogressTasks,
                    'completed':completedTasks,
                    'review':submittedForReviewTasks})


def CreateTask(request, projectID):
    try: 
        project = Project.objects.get(projectID=projectID)
    except:
        raise ObjectDoesNotExist
    if request.method == "POST":
        timestamp = datetime.now()
        assignee = request.POST['assignee'].split('-')
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
            managerID=project.managerID,
            status='I'
        )
        task.save()
    return redirect(reverse("ProjectDashboard", kwargs={"projectID": projectID}))


def TaskDashboard(request, taskID):
    task = Task.objects.get(taskID=taskID)
    reportForm = ReportForm(instance=task)
    if request.method == "POST":
        reportForm = ReportForm(request.POST, instance=task)
        if reportForm.is_valid():
            task = reportForm.save()
            task.status = 'R'
            task.completed = datetime.now()
            task.save()
            return redirect(reverse("ProjectDashboard", kwargs={"projectID":task.projectID}))
    return render(request, 'taskDashboard.html', {'form': reportForm, 'task':task})


def CreateTeam(request):
    if request.method == "POST":
        manager = request.POST['manager'].split('-')

        if request.POST['teamID']:
            team = Team.objects.get(teamID=request.POST['teamID'])
            team.name = request.POST['name']
            team.description = request.POST['description']
            team.managerID = manager[1]
            team.managerName = manager[0]
            team.save()
            return redirect(reverse("TeamDashboard", kwargs={"teamID": team.teamID}))

        timestamp = datetime.now()
        while Team.objects.filter(teamID="T"+timestamp.strftime("%H%M%S")):
            timestamp = datetime.now()

        team = Team(
            teamID="T"+timestamp.strftime("%H%M%S"),
            name=request.POST['name'],
            managerID=manager[1],
            managerName=manager[0],
            description=request.POST['description'],
        )
        team.save()
    return redirect("ManageTeams")


def ManageTeams(request):
    teams = Team.objects.all()
    managers = Employee.objects.filter(role='PM')
    return render(request, 'manageTeams.html', {'teams':teams, 'managers':managers})


def TeamDashboard(request, teamID):
    try: 
        team = Team.objects.get(teamID=teamID)
    except:
        raise ObjectDoesNotExist
    managers = Employee.objects.filter(role='PM')
    members = Employee.objects.filter(teamID=teamID, role='E')
    ongoingProjects = Project.objects.filter(teamID=teamID, status='O')
    completedProjects = Project.objects.filter(teamID=teamID, status='C')
    freeEmployees = Employee.objects.filter(teamID__isnull=True, role='E')
    return render(request, 'teamDashboard.html', {'team':team, 'managers':managers, 'members':members, 'freeEmployees':freeEmployees, 
                 'teamProjects':[("ongoing", "info", ongoingProjects),
                                 ("completed", "success", completedProjects)]})


def EditMembers(request, teamID):
    if request.method == "POST":
        if request.POST['type'] == 'add':
            toBeAdded = list(request.POST.keys())
            freeEmployees = Employee.objects.filter(teamID__isnull=True, role='E')
            for freeEmployee in freeEmployees:
                if freeEmployee.employeeID in toBeAdded:
                    freeEmployee.teamID = request.POST['teamID']
                    freeEmployee.teamName = request.POST['teamName']
                    freeEmployee.managerID = request.POST['managerID']
                    freeEmployee.managerName = request.POST['managerName']
                    freeEmployee.save()
        else:
            toBeRemoved = list(request.POST.keys())
            teamMembers = Employee.objects.filter(teamID=teamID, role='E')
            for teamMember in teamMembers:
                if teamMember.employeeID in toBeRemoved:
                    teamMember.teamID = None
                    teamMember.teamName = ""
                    teamMember.managerID = None
                    teamMember.managerName = ""
                    teamMember.save()
    
    return redirect(reverse("TeamDashboard", kwargs={"teamID": teamID}))


def Resources(request):
    return render(request, 'viewResources.html')


def RequestResource(request):
    return render(request, 'requestResource.html')


def ManageResources(request):
    return render(request, 'manageResources.html')

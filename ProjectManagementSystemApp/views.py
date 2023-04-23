from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.forms.models import model_to_dict


# Create your views here.



def Landing(request):
    if request.user.is_authenticated:
        return redirect('ViewProjects')
    return render(request, 'landing.html')

def Login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session.set_expiry(0)
            employee = model_to_dict(Employee.objects.get(employeeID=request.POST['username']))
            employee['joiningDate'] = employee['joiningDate'].strftime("%d-%m-%Y")
            request.session['employee'] = employee
            login(request, user)
            return redirect('ViewProjects')
        else:
            return redirect('Login')
    return render(request, 'login.html')

def Logout(request):
    request.session.flush()
    logout(request)
    return redirect('Landing')



# Only for Owner
@login_required
def CreateTeam(request):
    if request.session['employee']['role'] != 'O':
        raise PermissionDenied
    if request.method == "POST":
        manager = request.POST['manager'].split('-')

        if request.POST.get('teamID', ''):
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



# Owner and Project Manager
@login_required
def ManageTeams(request):
    userRole = request.session['employee']['role']
    if userRole != 'O' and userRole != 'PM':
        raise PermissionDenied

    if userRole == 'O':
        teams = Team.objects.all()
    else:
        teams = Team.objects.filter(managerID=request.session['employee']['employeeID'])

    managers = Employee.objects.filter(role='PM')
    return render(request, 'team/manageTeams.html', {'teams':teams, 'managers':managers})


# Owner, PM and Employee
@login_required
def TeamDashboard(request, teamID):
    userRole = request.session['employee']['role']
    if userRole != 'O' and userRole != 'PM' and userRole != 'E':
        raise PermissionDenied
    
    try: 
        team = Team.objects.get(teamID=teamID)
    except:
        raise ObjectDoesNotExist
    
    if userRole == 'PM' and team.managerID != request.session['employee']['employeeID']:
        raise PermissionDenied   

    managers = Employee.objects.filter(role='PM')
    members = Employee.objects.filter(teamID=teamID, role='E')
    ongoingProjects = Project.objects.filter(teamID=teamID, status='O')
    completedProjects = Project.objects.filter(teamID=teamID, status='C')
    freeEmployees = Employee.objects.filter(teamID__isnull=True, role='E')
    return render(request, 'team/teamDashboard.html', {'team':team, 'managers':managers, 'members':members, 'freeEmployees':freeEmployees, 
                 'teamProjects':[("ongoing", "info", ongoingProjects),
                                 ("completed", "success", completedProjects)]})


# Owner, Project Manager
@login_required
def EditMembers(request, teamID):
    userRole = request.session['employee']['role']
    if userRole != 'O' and userRole != 'PM':
        raise PermissionDenied
    
    try: 
        team = Team.objects.get(teamID=teamID)
    except:
        raise ObjectDoesNotExist

    if userRole != 'O' and team.managerID != request.session['employee']['employeeID']:
        raise PermissionDenied   

    if request.method == "POST":
        if request.POST['type'] == 'add':
            count = 0
            toBeAdded = list(request.POST.keys())
            freeEmployees = Employee.objects.filter(teamID__isnull=True, role='E')
            for freeEmployee in freeEmployees:
                if freeEmployee.employeeID in toBeAdded:
                    freeEmployee.teamID = team.teamID
                    freeEmployee.teamName = team.name
                    freeEmployee.managerID = team.managerID
                    freeEmployee.managerName = team.managerName
                    freeEmployee.save()
                    count = count + 1
            team.size = team.size + count
            team.save()
        else:
            count = 0
            toBeRemoved = list(request.POST.keys())
            teamMembers = Employee.objects.filter(teamID=teamID, role='E')
            for teamMember in teamMembers:
                if teamMember.employeeID in toBeRemoved:
                    teamMember.teamID = None
                    teamMember.teamName = ""
                    teamMember.managerID = None
                    teamMember.managerName = ""
                    teamMember.save()
                    count = count + 1
            team.size = team.size - count
            team.save()
    
    return redirect(reverse("TeamDashboard", kwargs={"teamID": teamID}))



# Only for Owner
@login_required
def CreateProject(request):
    if request.session['employee']['role'] != 'O':
        raise PermissionDenied
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
    return render(request, 'project/createProject.html', {'teams':teams})


@login_required
def EditProject(request, projectID):
    if request.session['employee']['role'] != 'O':
        raise PermissionDenied
    try:
        project = Project.objects.get(projectID=projectID)
    except:
        raise ObjectDoesNotExist
    
    teams = Team.objects.all()
    if request.method == "POST":
        team = teams.get(teamID=request.POST['team'])
        project.title = request.POST['title']
        project.client = request.POST['client']
        project.description = request.POST['description']
        project.allocatedBudget = request.POST['budget']
        project.deadline = request.POST['deadline']
        project.teamID = team.teamID,
        project.teamName = team.name,
        project.managerID = team.managerID,
        project.managerName = team.managerName,
        project.save()
        return redirect('ViewProjects')
    return render(request, 'project/createProject.html', {'teams':teams, 'project':project})



# As per employee type. PM, RM, E(Team-wise), Owner (All)  
@login_required
def ViewProjects(request):
    userRole = request.session['employee']['role']
    if userRole != 'O' and userRole != 'PM' and userRole != 'E':
        raise PermissionDenied
    
    if userRole == 'O':
        ongoingProjects = Project.objects.filter(status='O')
        completedProjects = Project.objects.filter(status='C')
    elif userRole == 'PM':
        ongoingProjects = Project.objects.filter(status='O', managerID=request.session['employee']['employeeID'])
        completedProjects = Project.objects.filter(status='C', managerID=request.session['employee']['employeeID'])
    elif userRole == 'E':
        ongoingProjects = Project.objects.filter(status='O', teamID=request.session['employee']['teamID'])
        completedProjects = Project.objects.filter(status='C', teamID=request.session['employee']['teamID'])

    return render(request, 'project/viewProjects.html', {'ongoingProjects':ongoingProjects, 'completedProjects':completedProjects})


@login_required
def ProjectDashboard(request, projectID):
    userRole = request.session['employee']['role']
    if userRole != 'O' and userRole != 'PM' and userRole != 'E':
        raise PermissionDenied
    
    try: 
        project = Project.objects.get(projectID=projectID)
    except:
        raise ObjectDoesNotExist

    if userRole == 'PM' and request.session['employee']['employeeID'] != project.managerID:
        raise PermissionDenied

    if userRole == 'E' and request.session['employee']["teamID"] != project.teamID:
        raise PermissionDenied

    teamMembers = Employee.objects.filter(role='E', teamID=project.teamID)

    if userRole == 'O' or userRole == 'PM':
        inprogressTasks = Task.objects.filter(projectID=projectID, status='I')
        completedTasks = Task.objects.filter(projectID=projectID, status='C')
        submittedForReviewTasks = Task.objects.filter(projectID=projectID, status='R')
    else:
        employeeID = request.session['employee']['employeeID']
        inprogressTasks = Task.objects.filter(projectID=projectID, status='I', employeeID=employeeID)
        completedTasks = Task.objects.filter(projectID=projectID, status='C', employeeID=employeeID)
        submittedForReviewTasks = Task.objects.filter(projectID=projectID, status='R', employeeID=employeeID)

    return render(request, 'project/projectDashboard.html', {'project':project, 'teamMembers':teamMembers, 
                    'inprogress': inprogressTasks,
                    'completed':completedTasks,
                    'review':submittedForReviewTasks})



@login_required
def CreateTask(request, projectID):
    try: 
        project = Project.objects.get(projectID=projectID)
    except:
        raise ObjectDoesNotExist
    
    userRole = request.session['employee']['role']
    if userRole != 'O' and userRole != 'PM':
        raise PermissionDenied
    
    if userRole == 'PM' and request.session['employee']['employeeID'] != project.managerID:
        raise PermissionDenied

    if request.method == "POST":
        assignee = request.POST['assignee'].split('-')
        if request.POST.get('taskID', ''):
            task = Task.objects.get(taskID=request.POST['taskID'])
            task.title = request.POST['title']
            task.description = request.POST['description']
            task.allocatedBudget = request.POST['budget']
            task.deadline = request.POST['deadline']
            task.employeeID = assignee[1]
            task.employeeName = assignee[0]
            task.save()
            return redirect(reverse("TaskDashboard", kwargs={"taskID": task.taskID}))
        
        timestamp = datetime.now()        
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
            teamID=project.teamID,
            status='I'
        )
        task.save()
    return redirect(reverse("ProjectDashboard", kwargs={"projectID": projectID}))


@login_required
def TaskDashboard(request, taskID):
    try:
        task = Task.objects.get(taskID=taskID)
    except:
        raise ObjectDoesNotExist
    
    userRole = request.session['employee']['role']
    if userRole != 'O' and userRole != 'PM' and userRole != 'E':
        raise PermissionDenied
    
    if userRole == 'PM' and request.session['employee']['employeeID'] != task.managerID:
        raise PermissionDenied
    
    if userRole == 'E' and request.session['employee']['employeeID'] != task.employeeID:
        raise PermissionDenied

    teamMembers = Employee.objects.filter(role='E', teamID=task.teamID)
    reportForm = ReportForm(instance=task)
    if request.method == "POST":
        if request.POST.get('review', '') == 'approved':
            if request.session['employee']['employeeID'] != task.managerID:
                raise PermissionDenied
            task.status = 'C'
            task.completed = datetime.now()
            task.save()
            return redirect(reverse("ProjectDashboard", kwargs={"projectID":task.projectID}))

        reportForm = ReportForm(request.POST, instance=task)
        if reportForm.is_valid():
            task = reportForm.save()
            task.status = 'R'
            task.submitted = datetime.now()
            task.save()
            return redirect(reverse("ProjectDashboard", kwargs={"projectID":task.projectID}))
    return render(request, 'task/taskDashboard.html', {'form': reportForm, 'task':task, 'teamMembers':teamMembers})



def Resources(request):
    return render(request, 'viewResources.html')


def RequestResource(request):
    return render(request, 'requestResource.html')


def ManageResources(request):
    return render(request, 'manageResources.html')

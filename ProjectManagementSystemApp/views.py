from django.shortcuts import render, redirect

# Create your views here.

def Home(request):
    return render(request, 'home.html')


def Landing(request):
    return render(request, 'landing.html')


def Login(request):
    return render(request, 'login.html')


def CreateProject(request):
    return render(request, 'createProject.html')


def CreateTeam(request):
    return render(request, 'createTeam.html')


def CreateTask(request):
    return render(request, 'createTask.html')


def SubmitReport(request):
    return render(request, 'submitReport.html')


def ViewProjects(request):
    return render(request, 'viewProjects.html')


def ProjectDashboard(request):
    return render(request, 'projectDashboard.html')


def ViewTeams(request):
    return render(request, 'viewTeams.html')


def TeamDashboard(request):
    return render(request, 'teamDashboard.html')


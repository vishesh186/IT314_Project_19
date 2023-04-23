from djongo import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from tinymce.models import HTMLField
from datetime import datetime
from django import forms
from django.forms import ModelForm

# Create your models here.

class Team(models.Model):
    teamID = models.SlugField(primary_key=True, max_length=10)
    name = models.CharField(max_length=64)
    description = models.TextField(default="")
    managerID = models.CharField(max_length=10)
    managerName = models.CharField(max_length=64)
    size = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.teamID


class Employee(models.Model):
    employeeID = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    joiningDate = models.DateField(null=True, blank=True)
    salary = models.PositiveIntegerField(default=0)
    role = models.CharField(max_length=6, default='E',
        choices=[
            ("PM", "Project Manager"),
            ("RM", "Resource Manager"),
            ("E", "Employee"),
            ("O", "Owner")
        ])
    teamID = models.CharField(null=True, blank=True, max_length=10)
    teamName = models.CharField(blank=True, max_length=64)
    managerID = models.CharField(null=True, blank=True, max_length=10)
    managerName = models.CharField(blank=True, max_length=64)

    def __str__(self):
        return self.employeeID
    
    def getBonus(self):
        if self.role == 'PM':
            return (self.salary)*0.15;
        else:
            return (self.salary)*0.10;




@receiver(post_save, sender=User)
def UpdateEmployee(sender, instance=None, created=False, **kwargs):
    if instance.is_staff:
       pass 
    if created:
        Employee.objects.create(
            employeeID=instance.username,
            name=instance.get_full_name(),
            email=instance.email
        )
    else:
        try:
            employee = Employee.objects.get(employeeID=instance.username)
            employee.employeeID = instance.username
            employee.name = instance.get_full_name()
            employee.email = instance.email
            employee.save()
        except:
            Employee.objects.create(
                employeeID=instance.username,
                name=instance.get_full_name(),
                email=instance.email
            )
    


class Project(models.Model):
    projectID = models.SlugField(primary_key=True, max_length=15)
    title = models.CharField(max_length=64)
    client = models.CharField(max_length=64)
    description = models.TextField()
    allocatedBudget = models.PositiveIntegerField(blank=True)
    utilizedBudget = models.PositiveIntegerField(blank=True, default=0)
    deadline = models.DateTimeField()
    created = models.DateTimeField(default=datetime.now())
    completed = models.DateTimeField(blank=True)
    status = models.CharField(max_length=1, default='O',
        choices=[
            ('O', 'Ongoing'),
            ('C', 'Completed'),
    ])
    
    teamID = models.CharField(blank=True, max_length=10)
    teamName = models.CharField(blank=True, max_length=64)
    managerID = models.CharField(blank=True, max_length=10)
    managerName = models.CharField(blank=True, max_length=64)

    def __str__(self):
        return self.projectID
    
    

class Task(models.Model):
    taskID = models.SlugField(primary_key=True, max_length=32)
    title = models.CharField(max_length=64)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True)
    submitted = models.DateTimeField(blank=True)
    completed = models.DateTimeField(blank=True)
    assigned = models.DateTimeField()
    allocatedBudget = models.PositiveIntegerField()
    utilizedBudget = models.PositiveIntegerField(null=True, blank=True)
    report = HTMLField(blank=True)
    employeeID = models.SlugField(max_length=10)
    employeeName = models.CharField(max_length=64)
    projectID = models.SlugField(max_length=15)
    managerID = models.SlugField(max_length=10)
    teamID = models.SlugField(max_length=10)
    status = models.CharField(max_length=1, default='I',
        choices=[
            ('I', 'In Progress'),
            ('C', 'Completed'),
            ('R', 'Submitted For Review')
    ])
 
    def __str__(self):
        return self.taskID
    


class ReportForm(ModelForm):
    class Meta:
        model = Task
        fields = ['report', 'utilizedBudget']

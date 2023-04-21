from djongo import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms import ModelForm
from tinymce.models import HTMLField


# Create your models here.

class Team(models.Model):
    teamID = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=64)
    managerID = models.CharField(max_length=10)
    managerName = models.CharField(max_length=64)

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
        ])
    team = models.EmbeddedField(null=True, blank=True, model_container=Team)
    objects = models.DjongoManager()

    def __str__(self):
        return self.employeeID
    
    def getBonus(self):
        if self.role == 'PM':
            return (self.salary)*0.15;
        else:
            return (self.salary)*0.10;



@receiver(post_save, sender=User)
def UpdateEmployee(sender, instance=None, created=False, **kwargs):
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
    budget = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    team = models.EmbeddedField(model_container=Team, null=True)

    def __str__(self):
        return self.projectID
    

class Task(models.Model):
    taskID = models.SlugField(primary_key=True, max_length=32)
    title = models.CharField(max_length=64)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True)
    completed = models.DateTimeField(blank=True)
    assigned = models.DateTimeField()
    allocatedBudget = models.PositiveIntegerField()
    utilizedBudget = models.PositiveIntegerField(null=True, blank=True)
    report = HTMLField(blank=True)
    employeeID = models.CharField(max_length=10)
    employeeName = models.CharField(max_length=64)
    projectID = models.SlugField(max_length=15)
    managerID = models.CharField(max_length=10)
    status = models.CharField(max_length=1, default='I',
        choices=[
            ('I', 'In Progress'),
            ('C', 'Completed'),
            ('R', 'Submitted For Review')
    ])
 
    def __str__(self):
        return self.taskID
    

class Resources(models.Model):
    resourceID = models.SlugField(primary_key=True, max_length=32)
    title = models.CharField(max_length=64)
    count = models.IntegerField()
    availability = models.BooleanField()
    bookedby = models.EmbeddedField(model_container=Employee, model_form_class=EmployeeForm)
    bookingfrom = models.DateTimeField()
    bookingtill = models.DateTimeField()

    def __str__(self):
        return self.resourceID
    
class File(models.Model):
    fileID = models.SlugField(primary_key=True, max_length=32)
    filename = models.CharField(max_length=64)
    uploadedby = models.EmbeddedField(model_container=Employee, model_form_class=EmployeeForm)
    uploadedat = models.DateTimeField()

    def __str__(self):
        return self.fileID

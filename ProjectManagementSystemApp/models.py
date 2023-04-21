from djongo import models

# Create your models here.
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


    def __str__(self):
        return self.employeeID
    

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['employeeID', 'name', 'email', 'role']


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
    projectID = models.SlugField(primary_key=True, max_length=32)
    title = models.CharField(max_length=64)
    client = models.CharField(max_length=64)
    description = models.TextField()
    budget = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    manager = models.EmbeddedField(model_container=Employee, model_form_class=EmployeeForm)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    taskID = models.SlugField(primary_key=True, max_length=32)
    title = models.CharField(max_length=64)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True)
    completed = models.DateTimeField(blank=True)
    assigned = models.BooleanField(default=False)
    assignedTo = models.EmbeddedField(model_container=Employee)

    def __str__(self):
        return self.title

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

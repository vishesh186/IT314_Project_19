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

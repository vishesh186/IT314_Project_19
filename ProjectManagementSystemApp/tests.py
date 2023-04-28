

from django.test import TestCase
from .models import Employee

from sqlite3 import Date
from django.test import TestCase

import datetime

from django.test import SimpleTestCase

from django.urls import reverse, resolve

from ProjectManagementSystemApp.views import Landing

from rest_framework.test import APIClient, APITestCase


from ProjectManagementSystemApp.models import Resource

from django.utils import timezone
# Create your tests here.


class EmployeeTestCase(TestCase):
    def setUp(self):
        elon = Employee.objects.create(
            employeeID='001', name='Elon Musk', email='elon@musk.com', salary=100000, role='PM')
        tim = Employee.objects.create(
            employeeID='002', name='Tim Cook', email='tim@cook.com', salary=90000, role='E')
        anil = Employee.objects.create(
            employeeID='003', name='Anil Ambani', email='anil@ambani.com', salary=70000, role='RM')

    def testEmployeeBonus(self):
        elon = Employee.objects.get(employeeID='001')
        tim = Employee.objects.get(employeeID='002')
        anil = Employee.objects.get(employeeID='003')
       # self.assertTrue(elon.getBonus()==14000, 'bonus should be 15000')
        self.assertEqual(tim.getBonus(), 9000)
        self.assertEqual(anil.getBonus(), 7000)
        self.assertEqual(anil.getTeamId(), None)


class UnitTesting(TestCase):

    def setUp(self) -> None:
        print('setup called')

    def test_employee_email(self):

        emails = ["kashaypsojitra30@gmail.com",
                  "iammaher@gmail.com"]

        employee1 = Employee.objects.create(
            employeeID="EMP001",
            name="John Doe",
            email=emails[0],
            joiningDate=Date(2020, 1, 1),
            salary=50000,
            role="E",
            teamID="TEAM001",
            teamName="Engineering",
            managerID="MAN001",
            managerName="Jane Smith"
        )
        employee2 = Employee.objects.create(
            employeeID="EMP002",
            name="ron Doe",
            email=emails[1],
            joiningDate=Date(2020, 3, 12),
            salary=50000,
            role="M",
            teamID="TEAM005",
            teamName="Managering",
            managerID="MAN005",
            managerName="Jane watson"
        )
        self.assertEquals("kashaypsojitra30@gmail.com", employee1.email)

        self.assertEquals("iammaher@gmail.com", employee2.email)

        objs = Employee.objects.all()

        self.assertEquals(objs.count(), 2)


class ProjectTestCase(APITestCase):

    def tearDown(self) -> None:
        pass

    def setUp(self) -> None:
        obj = Project.objects.create (
            projectID = '4363',title = 'Test Project',client = 'demo client',description = 'demo project',
            allocatedBudget = '200000',status = 'O',deadline = datetime.datetime(2023, 5, 1, 23, 59, 59, tzinfo=datetime.timezone.utc))
        

    def test_project(self):
        obj = Project.objects.get(projectID = '4363')
        self.assertEqual(obj.allocatedBudget , 200000)
        self.assertEqual(obj.deadline,datetime.datetime(2023, 5, 1, 23, 59, 59, tzinfo=datetime.timezone.utc))
        self.assertEqual(obj.status,'O')
        self.assertGreaterEqual(obj.deadline,datetime.datetime(2023,4, 1, 23, 59, 59, tzinfo=datetime.timezone.utc)) 
        second argument is actual completion time of project and first argument is given deadline for project



class TeamTestCase(TestCase):
          def setUp(self):
            mer = Team.objects.create(teamID='5050',name='demo team',
                                  managerID='7506',managerName='kashyap',size='10')
        
          def testTeam(self):
            mer = Team.objects.get(teamID='5050')
            self.assertEqual(mer.getTeamSize(),10)  





class ResourceModelTestCase(TestCase):
    def setUp(self):
        self.resource = Resource.objects.create(
            resourceID='res-001',
            name='Meeting Room 1',
            bookingPurpose='Project review meeting',
            bookingType='Booking Type',
            bookedByID = '5050',
            bookedByName = 'ketan',
            created=timezone.now()
        )
    
    def test_resource_creation(self):
        self.assertEqual(self.resource.resourceID, 'res-001')
        self.assertEqual(self.resource.name, 'Meeting Room 1')
        self.assertEqual(self.resource.status, 'A')
        self.assertEqual(self.resource.bookingPurpose, 'Project review meeting')
        self.assertEqual(self.resource.bookingType, 'Booking Type')
        self.assertEqual(self.resource.bookedByID, '5050')
        self.assertEqual(self.resource.bookedByName, 'ketan')
        self.assertEqual(self.resource.bookedFrom, None)
        self.assertEqual(self.resource.bookedTill, None)
        self.assertTrue(isinstance(self.resource.created, timezone.datetime))

           

class EmployeeTestCase(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(employeeID='E001', name='John Doe', email='johndoe@example.com', joiningDate='2022-01-01', salary=50000, role='E')

    def test_getBonus(self):
        bonus = self.employee.getBonus()
        self.assertEqual(bonus, 5000) # 10% of salary for non-PM employees

        self.employee.role = 'PM'
        self.employee.save()
        bonus = self.employee.getBonus()
        self.assertEqual(bonus, 7500) # 15% of salary for PM employees

    def test_updateRating(self):
        self.assertEqual(self.employee.avgRating, None) # avgRating should be None initially

        # create two tasks with different ratings for the employee
        from .models import Task
        Task.objects.create(taskID='T001', title='Task 1', description='Task 1 description', employeeID=self.employee, rating=4)
        Task.objects.create(taskID='T002', title='Task 2', description='Task 2 description', employeeID=self.employee, rating=3)

        self.employee.updateRating()
        self.assertEqual(self.employee.avgRating, 3.5) # average of 4 and 3 is 3.5

        # create another task with a different rating and update the employee's rating again
        Task.objects.create(taskID='T003', title='Task 3', description='Task 3 description', employeeID=self.employee, rating=5)
        self.employee.updateRating()
        self.assertEqual(self.employee.avgRating, 4) # average of 4, 3, and 5 is 4

from django.test import TestCase

# Create your tests here.
from django.test import TestCase


# Create your tests here.

from django.test import TestCase
from .models import Employee

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

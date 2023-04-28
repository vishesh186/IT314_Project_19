

# from ProjectManagementSystemApp.models import Project, Task, Team

# from django.urls import reverse

# from datetime import datetime

# from django.test import TestCase, Client



# class CreateProjectViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.team = Team.objects.create(
#             name='Test Team',
#             managerName='Test Manager',
#             managerID='123',
#         )

#     def test_create_project(self):
#         url = '/create-project/'
#         data = {
#             'title': 'Test Project',
#             'client': 'Test Client',
#             'description': 'Test Description',
#             'budget': 10000,
#             'deadline': '2023-05-01',
#             'teamID': self.team.teamID,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)  # redirect status code
#         project = Project.objects.first()
#         self.assertEqual(project.title, 'Test Project')
#         self.assertEqual(project.client, 'Test Client')
#         self.assertEqual(project.description, 'Test Description')
#         self.assertEqual(project.allocatedBudget, 10000)
#         self.assertEqual(project.deadline.strftime('%Y-%m-%d'), '2023-05-01')
#         self.assertEqual(project.teamID, self.team.teamID)
#         self.assertEqual(project.teamName, 'Test Team')
#         self.assertEqual(project.managerID, '123')
#         self.assertEqual(project.managerName, 'Test Manager')
#         self.assertEqual(project.status, 'O')


# class CreateTaskViewTest(TestCase):
#     def setUp(self):
#         self.project = Project.objects.create(
#             projectID="1234",
#             title="Test Project",
#             managerID="MGR01",
#             description="Test description"
#         )

#     def test_create_task(self):
#         url = reverse('CreateTask')
#         data = {
#             'value':'1234',
#             'title': 'Test Task',
#             'budget': 100,
#             'description': 'Test task description',
#             'assignee': 'John Doe-MGR01',
#             'deadline': datetime.now().strftime("%Y-%m-%d"),
#         }
#         response = self.client.post(url, data)
#         print(response.status_code)    
#         self.assertEqual(response.status_code, 302)  # expect a redirect
#         self.assertEqual(Task.objects.count(), 1)  # expect a new task to be created

#         task = Task.objects.first()
#         self.assertEqual(task.title, data['title'])
#         self.assertEqual(task.allocatedBudget, data['budget'])
#         self.assertEqual(task.description, data['description'])
#         self.assertEqual(task.employeeName, 'John Doe')
#         self.assertEqual(task.employeeID, 'MGR01')
#         self.assertEqual(task.deadline.strftime("%Y-%m-%d"), data['deadline'])
#         self.assertEqual(task.projectID, self.project.projectID)
#         self.assertEqual(task.managerID, self.project.managerID)
#         self.assertEqual(task.status, 'I')

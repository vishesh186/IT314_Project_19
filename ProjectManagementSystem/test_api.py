
from django.test import SimpleTestCase

from django.urls import reverse , resolve

from ProjectManagementSystemApp.views import Landing

from rest_framework.test import APIClient , APITestCase

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from rest_framework import status


class ApiUrlTests(SimpleTestCase):

    def test_get_landingPage(self):
        url = reverse('Landing')
        print(resolve(url).func)
        self.assertEquals(resolve(url).func,Landing)

 
class viewProjectsAPIViewTests(APITestCase):


    view_projects_urls = reverse('ViewProjects')
    print(resolve(view_projects_urls).func)

    def tearDown(self) -> None:
        pass
    
    def test_get_projectinfoPage(self):
        
        response = self.client.get(self.view_projects_urls);
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  
         
          
       class TeamTestCase(TestCase):
          def setUp(self):
          mer = Team.objects.create(teamID='5050',name='ketan',discription='this is a team for course project',
                                  managerID='7506',managerName='kashyap',size='10')
        
        def testTeam(self):
            mer = Team.objects.get(teamID='5050')
            self.assertEqual(mer.getTeamSize(), 10)   

 class LandingAPIViewTests(APITestCase):
   
    landing_urls = reverse('Landing')

    def tearDown(self) -> None:
        pass
    
    def test_get_landingPage(self):
        response = self.client.get(self.landing_urls);
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
  
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
        
        
class CreateProjectTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.team = Team.objects.create(
            name='Test Team',
            managerName='Test Manager',
            managerID='123',
        )

    def test_create_project(self):
        url = '/create-project/'
        data = {
            'title': 'Test Project',
            'client': 'Test Client',
            'description': 'Test Description',
            'budget': 10000,
            'deadline': '2023-05-01',
            'teamID': self.team.teamID,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # redirect status code
        project = Project.objects.first()
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.client, 'Test Client')
        self.assertEqual(project.description, 'Test Description')
        self.assertEqual(project.allocatedBudget, 10000)
        self.assertEqual(project.deadline.strftime('%Y-%m-%d'), '2023-05-01')
        self.assertEqual(project.teamID, self.team.teamID)
        self.assertEqual(project.teamName, 'Test Team')
        self.assertEqual(project.managerID, '123')
        self.assertEqual(project.managerName, 'Test Manager')
        self.assertEqual(project.status, 'O')

class CreateTaskViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            projectID="1234",
            title="Test Project",
            managerID="MGR01",
            description="Test description"
        )

    def test_create_task(self):
        url = reverse('CreateTask')
        data = {
            'value':'1234',
            'title': 'Test Task',
            'budget': 100,
            'description': 'Test task description',
            'assignee': 'John Doe-MGR01',
            'deadline': datetime.now().strftime("%Y-%m-%d"),
        }
        response = self.client.post(url, data)
        print(response.status_code)    
        self.assertEqual(response.status_code, 302)  # expect a redirect
        self.assertEqual(Task.objects.count(), 1)  # expect a new task to be created

        task = Task.objects.first()
        self.assertEqual(task.title, data['title'])
        self.assertEqual(task.allocatedBudget, data['budget'])
        self.assertEqual(task.description, data['description'])
        self.assertEqual(task.employeeName, 'John Doe')
        self.assertEqual(task.employeeID, 'MGR01')
        self.assertEqual(task.deadline.strftime("%Y-%m-%d"), data['deadline'])
        self.assertEqual(task.projectID, self.project.projectID)
        self.assertEqual(task.managerID, self.project.managerID)
        self.assertEqual(task.status, 'I')

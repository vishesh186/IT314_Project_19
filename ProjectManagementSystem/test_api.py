
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

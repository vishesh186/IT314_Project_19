
import json
from django.test import SimpleTestCase, TestCase
from requests import request

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import resolve, reverse
from ProjectManagementSystemApp.models import Employee, Project, Team

from django.test import Client


from django.test import TestCase, Client
from django.urls import reverse

from ProjectManagementSystemApp.views import Landing




# class ApiUrlTests(SimpleTestCase):

#     def test_get_landingPage(self):
#         url = reverse('Landing')
#         print(resolve(url).func)
#         self.assertEquals(resolve(url).func,Landing)


# class LandingAPIViewTests(APITestCase):

#     landing_urls = reverse('Landing')

#     def tearDown(self) -> None:
#         pass

#     def test_get_landingPage(self):
#         response = self.client.get(self.landing_urls);
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


    
# class viewProjectsAPIViewTests(APITestCase):


#     view_projects_urls = reverse('ViewProjects')
#     print(resolve(view_projects_urls).func)

#     def tearDown(self) -> None:
#         pass

#     def test_get_projectinfoPage(self):

#         response = self.client.get(self.view_projects_urls);
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class ViewTeamsTestCase(TestCase):

    def tearDown(self) -> None:
         pass

    def test_view_teams(self):
        url = reverse('ViewTeams') # assuming the view name is 'view_teams'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewTeams.html')



# error


# class TeamDashboardTestCase(TestCase):
    
#     def setUp(self):
#         self.team = Team.objects.create(teamID=1, name='Test Team')
#         self.pm = Employee.objects.create(employeeID=1, name='Test PM', role='PM')
#         self.member = Employee.objects.create(employeeID=2, name='Test Member', teamID=self.team, role='E')
#         self.free_employee = Employee.objects.create(employeeID=3, name='Test Free Employee', role='E')
#         self.ongoing_project = Project.objects.create(projectID=1, title='Ongoing Project', teamID=self.team, status='O')
#         self.completed_project = Project.objects.create(projectID=2, title='Completed Project', teamID=self.team, status='C')
        
#     def test_team_dashboard(self):
#         url = reverse('TeamDashboard', args=[self.team.teamID])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'teamDashboard.html')
#         self.assertEqual(response.context['team'], self.team)
#         self.assertQuerysetEqual(response.context['managers'], [repr(self.pm)])
#         self.assertQuerysetEqual(response.context['members'], [repr(self.member)])
#         self.assertQuerysetEqual(response.context['freeEmployees'], [repr(self.free_employee)])
#         self.assertEqual(response.context['teamProjects'][0][0], 'ongoing')
#         self.assertEqual(response.context['teamProjects'][0][1], 'info')
#         self.assertQuerysetEqual(response.context['teamProjects'][0][2], [repr(self.ongoing_project)])
#         self.assertEqual(response.context['teamProjects'][1][0], 'completed')
#         self.assertEqual(response.context['teamProjects'][1][1], 'success')
#         self.assertQuerysetEqual(response.context['teamProjects'][1][2], [repr(self.completed_project)])


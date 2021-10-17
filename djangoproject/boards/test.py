from .views import home
from  django.urls import reverse
from django.test import TestCase
from django.urls.base import resolve

class HomeTest(TestCase):
    def test_home_view_status_code(self):
        url=reverse('home')
        response=self.client.get(url)
        self.assertEquals(response.status_code,200)

    # Check the correct view function for the requested url
    def test_home_resolves_home_view(self):
        view=resolve('/')
        self.assertEquals(view.func,home)

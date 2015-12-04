from django.test.client import Client
from django.test import TestCase
import re
from django.test import LiveServerTestCase
from selenium import webdriver
import os
class HomeTest(TestCase):
    fixtures = ["cities.json"]

    def test_has_world(self):
        c = Client()

        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "world")

    def test_has_amsterdam(self):
        c = Client()

        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amsterdam")


class MySeleniumTests(LiveServerTestCase):
    fixtures = ["data/locations.json"]

    @classmethod
    def setUpClass(cls):
        chromedriver = "/usr/local/bin/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        cls.selenium = webdriver.Chrome(chromedriver)
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_locations(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/locations/'))
        src = self.selenium.page_source
        text_found = re.search(r'text_to_search', src)
        self.assertFalse(text_found)
        text_found = re.search(r'Amsterdam', src)
        self.assertTrue(text_found)

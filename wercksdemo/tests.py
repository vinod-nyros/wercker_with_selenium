from django.test.client import Client
from django.test import TestCase
import re

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()


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
        binary = FirefoxBinary('/usr/bin/firefox')
        cls.selenium = webdriver.Firefox(firefox_binary=binary)
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

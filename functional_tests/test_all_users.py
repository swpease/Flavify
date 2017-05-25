from selenium import webdriver

from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(NewVisitorTest, cls).setUpClass()
        cls.browser = webdriver.Firefox(executable_path="/Users/Scott/BrowserDrivers/geckodriver")
        cls.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(NewVisitorTest, cls).tearDownClass()

    def get_full_url(self, path):
        return self.live_server_url + reverse(path)

    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("Flavify", self.browser.title)

    def test_h1_css(self):
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"), "rgb(200, 50, 255)")
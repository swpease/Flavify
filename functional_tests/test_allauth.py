from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# https://stackoverflow.com/questions/10404160/when-to-use-explicit-wait-vs-implicit-wait-in-selenium-webdriver
class TestAllauth(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAllauth, cls).setUpClass()
        cls.browser = webdriver.Firefox(executable_path="/Users/Scott/BrowserDrivers/geckodriver")
        cls.browser.wait = WebDriverWait(cls.browser, 10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(TestAllauth, cls).tearDownClass()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
            (By.ID, element_id)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
            (By.ID, element_id)))

    def get_elements_by_class(self, html_class):
        return self.browser.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, html_class)))

    def get_element_by_class(self, html_class):
        return self.browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, html_class)))


    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    # BEGIN ACTUAL TESTS
    def test_login(self):
        # Just checking that the Bootstrap is correctly integrated with the allauth.
        self.browser.get(self.get_full_url("account_login"))
        bootstrap_forms = self.get_elements_by_class("form-group")
        self.assertEqual(len(bootstrap_forms), 4)
        forms_el_mark = self.get_elements_by_class("form-control")
        self.assertEqual(len(forms_el_mark), 2)
        sr = self.get_elements_by_class("sr-only")
        self.assertEqual(len(sr), 3)

    def test_signup(self):
        self.browser.get(self.get_full_url("account_signup"))
        form_wrapper = self.get_elements_by_class("form-group")
        self.assertEqual(len(form_wrapper), 5)
        forms_el_mark = self.get_elements_by_class("form-control")
        self.assertEqual(len(forms_el_mark), 4)
        sr = self.get_elements_by_class("sr-only")
        self.assertEqual(len(sr), 5)

    def test_logout(self):
        pass

    # NOT SURE HOW TO GET THIS TO WORK
    # def test_social_signup(self):
    #     self.browser.get(self.get_full_url("account_signup"))
    #     twitter_icon = self.get_element_by_class("twitter")
    #     ActionChains(self.browser).click(twitter_icon).perform()
    #     form_wrapper = self.get_elements_by_class("form-groupsadg")
    #     self.assertEqual(len(form_wrapper), 3)
    #     forms_el_mark = self.get_elements_by_class("form-control")
    #     self.assertEqual(len(forms_el_mark), 2)
    #     sr = self.get_elements_by_class("sr-only")
    #     self.assertEqual(len(sr), 3)


        # def test_google_login(self):
    #     self.browser.get(self.get_full_url("home"))
    #     google_login = self.get_element_by_id("google_login")
    #     with self.assertRaises(TimeoutException):
    #         self.get_element_by_id("logout")
    #     self.assertEqual(
    #         google_login.get_attribute("href"),
    #         self.live_server_url + "/accounts/google/login")
    #     google_login.click()
    #     with self.assertRaises(TimeoutException):
    #         self.get_element_by_id("google_login")
    #     google_logout = self.get_element_by_id("logout")
    #     google_logout.click()
    #     google_login = self.get_element_by_id("google_login")

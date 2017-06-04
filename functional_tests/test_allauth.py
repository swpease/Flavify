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

    def signup(self):
        self.browser.get(self.get_full_url("account_signup"))
        username = self.get_element_by_id("id_username")
        email = self.get_element_by_id("id_email")
        pw1 = self.get_element_by_id("id_password1")
        pw2 = self.get_element_by_id("id_password2")
        btn = self.browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-group .btn")))
        ac = ActionChains(self.browser)
        ac.send_keys_to_element(username, "me")
        ac.send_keys_to_element(email, "x@y.com")
        ac.send_keys_to_element(pw1, "terriblepw")
        ac.send_keys_to_element(pw2, "terriblepw")
        ac.click(btn)

    def signin(self):
        # self.browser.get(self.get_full_url("account_login"))
        username = self.get_element_by_id("id_login")
        pw = self.get_element_by_id("id_password")
        remember = self.get_element_by_id("id_remember")
        btn = self.browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-group .btn")))
        ActionChains(self.browser).send_keys_to_element(
            username, "me").send_keys_to_element(
            pw, "terriblepw").click(
            btn).perform()

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

    # def test_logout(self):
    #     pass

    def test_password_reset(self):
        # self.signup()
        self.browser.get(self.get_full_url("account_reset_password"))
        form_wrapper = self.get_elements_by_class("form-group")
        self.assertEqual(len(form_wrapper), 1)
        forms_el_mark = self.get_elements_by_class("form-control")
        self.assertEqual(len(forms_el_mark), 1)
        sr = self.get_elements_by_class("sr-only")
        self.assertEqual(len(sr), 2)

    def test_password_change(self):
        self.signup()
        self.browser.get(self.get_full_url("account_change_password"))
        self.signin()
        form_wrapper = self.get_elements_by_class("form-groups")
        self.assertEqual(len(form_wrapper), 3)
        forms_el_mark = self.get_elements_by_class("form-control")
        self.assertEqual(len(forms_el_mark), 3)
        sr = self.get_elements_by_class("sr-only")
        self.assertEqual(len(sr), 4)


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
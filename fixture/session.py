from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_css_selector("input[type='submit']").click()
        WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.NAME, "password")))
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector("input[type='submit']").click()

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)

    def is_logged_in(self):
        wd = self.app.wd
        return wd.find_elements_by_xpath("//a[contains(@href, 'logout_page.php')]")

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("li[class='grey'] a span").text

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_css_selector('span[class="user-info"]').click()
        wd.find_element_by_xpath("//a[contains(text(), 'Logout')]").click()
        WebDriverWait(wd, 5).until(EC.visibility_of_element_located((By.NAME, "username")))

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()



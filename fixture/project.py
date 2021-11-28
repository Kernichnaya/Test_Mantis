import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from model.project import Project


class ProjectHelper:

    project_cache = None

    def __init__(self, app):
        self.app = app

    def open_manage_project_page(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href, 'manage_overview_page.php')]").click()
        wd.find_element_by_xpath("//a[contains(@href, 'manage_proj_page.php')]").click()

    def create_new_project(self, project: Project):
        wd = self.app.wd
        self.open_manage_project_page()
        WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
        wd.find_element_by_xpath('//button[@type="submit"]').click()
        WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.ID, 'project-name')))
        self.fill_new_project_form(project)
        wd.find_element_by_css_selector('input[value="Add Project"]').click()
        if wd.find_elements_by_xpath('//div[@class="alert alert-danger"]'):
           raise Exception(f"Проект с названием {project.name} уже существует")
        self.open_manage_project_page()
        self.project_cache = None

    def fill_new_project_form(self, project: Project):
        wd = self.app.wd
        wd.find_element_by_xpath('//input[@id="project-name"]').click()
        wd.find_element_by_xpath('//input[@id="project-name"]').clear()
        wd.find_element_by_xpath('//input[@id="project-name"]').send_keys(project.name)
        wd.find_element_by_css_selector(f"select[name='status'] option[value='{project.status_code}']").click()
        wd.find_element_by_css_selector(f"select[name='view_state'] option[value='{project.view_state_code}']").click()
        wd.find_element_by_xpath('//textarea[@id="project-description"]').click()
        wd.find_element_by_xpath('//textarea[@id="project-description"]').clear()
        wd.find_element_by_xpath('//textarea[@id="project-description"]').send_keys(project.description)

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_project_page()
            self.project_cache = []
            table_rows = wd.find_elements_by_xpath('//div[@class="table-responsive"]/table/tbody/tr')
            category_list = wd.find_elements_by_xpath('//div[@id="categories"]/div/div[@class="widget-body"]/div/div[@class="table-responsive"]/table/tbody/tr')
            table_rows = [row for row in table_rows if row not in category_list]
            for row in table_rows:
                columns = row.find_elements_by_tag_name("td")
                project_link = row.find_element_by_tag_name('a').get_attribute('href')
                id = project_link[project_link.find('=') + 1:]
                self.project_cache.append(Project(id=id,
                                                  name=columns[0].text,
                                                  status=columns[1].text,
                                                  view_state=columns[3].text,
                                                  description=columns[4].text))
            return self.project_cache
        return list(self.project_cache)

    def delete_project_by_id(self, project_id: str):
        wd = self.app.wd
        self.open_manage_project_page()
        wd.find_element_by_xpath(f'//a[contains(@href, "manage_proj_edit_page.php?project_id={project_id}")]').click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click() # confirm the operation on the yellow screen
        self.open_manage_project_page()
        self.project_cache = None
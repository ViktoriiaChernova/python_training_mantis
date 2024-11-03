from selenium.webdriver.support.ui import Select
from model.project import Project
from urllib.parse import urlparse, parse_qs

class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def create(self, project):
            wd = self.app.wd
            wd.find_element_by_name("name").click()
            wd.find_element_by_name("name").clear()
            wd.find_element_by_name("name").send_keys(project.name)
            wd.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='*'])[1]/following::td[2]").click()
            Select(wd.find_element_by_name("status")).select_by_visible_text(project.status)
            wd.find_element_by_xpath("//option[@value='30']").click()
            wd.find_element_by_name("inherit_global").click()
            Select(wd.find_element_by_name("view_state")).select_by_visible_text(project.view_status)
            wd.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='View Status'])[1]/following::option[2]").click()
            wd.find_element_by_name("description").click()
            wd.find_element_by_name("description").clear()
            wd.find_element_by_name("description").send_keys(project.description)
            wd.find_element_by_xpath("//input[@value='Add Project']").click()
            wd.find_element_by_xpath("//input[@value='Create New Project']")
            self.open_projects_page()

    def get_projects_list(self):
        wd = self.app.wd
        self.open_projects_page()
        self.projects_list = []
        not_filtered_list = wd.find_elements_by_css_selector(".row-1, .row-2")
        filtered_list = [element for element in not_filtered_list if "General" not in element.text]
        for element in filtered_list:
            ids = element.find_element_by_xpath(".//td//a[contains(@href, 'manage_proj_edit_page.php?project_id=')]")
            href = ids.get_attribute('href')
            parsed_url = urlparse(href)
            query_params = parse_qs(parsed_url.query)
            id = query_params.get('project_id', [None])[0]
            name = element.find_element_by_xpath(".//td//a[contains(@href, 'manage_proj_edit_page.php?project_id=')]").text
            status = element.find_element_by_css_selector("td:nth-child(2)").text
            view_status = element.find_element_by_css_selector("td:nth-child(4)").text
            description = element.find_element_by_css_selector("td:nth-child(5)").text
            self.projects_list.append(Project(id=id, name=name, status=status, view_status=view_status, description=description))
        return list(self.projects_list)

    def open_new_project_form(self):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        title_form_name = wd.find_element_by_css_selector("td.form-title").text
        assert title_form_name == "Add Project"

    def open_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()

        self.project_cache = None

    def delete_by_name(self, name):
            wd = self.app.wd
            wd.find_element_by_link_text(name).click()
            wd.find_element_by_xpath("//input[@value='Delete Project']").click()
            wd.find_element_by_xpath("//input[@value='Delete Project']").click()

    def delete_project_by_index(self, index):
            wd = self.app.wd
            wd.find_elements_by_xpath(".//td//a[contains(@href, 'manage_proj_edit_page.php?project_id=')]")[
                index].click()
            wd.find_element_by_xpath("//input[@value='Delete Project']").click()
            wd.find_element_by_xpath("//input[@value='Delete Project']").click()

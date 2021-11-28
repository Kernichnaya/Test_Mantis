from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app
        self.client = Client('http://localhost/mantisbt-2.25.2/api/soap/mantisconnect.php?wsdl')
        self.username = self.app.config['webAdmin']['username']
        self.password = self.app.config['webAdmin']['password']

    def can_login(self, username, password):
        try:
            self.client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self):
        try:
            projects_list = self.client.service.mc_projects_get_user_accessible(self.username, self.password)
            return list(map(lambda x: self.convert_project_from_soap_to_model(x), projects_list))
        except WebFault:
            return []

    def convert_project_from_soap_to_model(self, project_data):
        return Project(id=str(project_data.id),
                       name=str(project_data.name),
                       status=str(project_data.status.name),
                       view_state=str(project_data.view_state.name),
                       description=str(project_data.description))
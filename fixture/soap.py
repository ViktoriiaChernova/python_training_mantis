from suds.client import Client
from suds import WebFault

class SoapHelper:

    def __init__(self, app, base_url):
        self.app = app
        self.base_url = base_url


    def can_login(self, username, password):
        client = Client(f"{self.base_url}api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, username, password):
        client = Client(f"{self.base_url}api/soap/mantisconnect.php?wsdl")
        return client.service.mc_projects_get_user_accessible(username, password)
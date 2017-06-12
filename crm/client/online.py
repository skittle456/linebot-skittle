import configparser
import os

import adal
import requests

cur_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(os.path.dirname(cur_dir)), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

user = config['CRM']['UserName']
password = config['CRM']['Password']
api_url = config['CRM']['ServiceURL']
base_url = config['CRM']['BaseURI']
auth_url = config['CRM']['AuthURI']
client_id = config['CRM']['ClientID']

RESOURCE = base_url
context = adal.AuthenticationContext(auth_url)


class CRMClient(object):
    token = None
    headers = None
    session = requests.Session()

    def __init__(self):
        self.token = context.acquire_token_with_username_password(
            RESOURCE,
            user,
            password,
            client_id)
        # print(self.token)
        return

    def refresh_access(self):
        refresh_token = self.token['refreshToken']
        self.token = context.acquire_token_with_refresh_token(
            refresh_token,
            client_id,
            RESOURCE)
        # print(self.token)
        self.headers = {
            'Authorization': 'Bearer %s' % self.token['accessToken'],
            'Content-Type': 'application/json; charset=utf-8',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
        }
        return

    def get(self, path=''):
        self.refresh_access()
        response = self.session.get(url=api_url + path, headers=self.headers)
        print(response)
        return response

    def post(self, path='', data=None):
        self.refresh_access()
        response = self.session.post(url=api_url + path, headers=self.headers, data=data)
        print(response)
        return response

    def patch(self, path='', data=None):
        self.refresh_access()
        response = self.session.patch(url=api_url + path, headers=self.headers, data=data)
        print(response)
        return response

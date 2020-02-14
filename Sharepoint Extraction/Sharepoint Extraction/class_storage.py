import requests
from requests_ntlm import HttpNtlmAuth
from urllib.parse import urljoin

class SharepointConnector:
    def __init__(self, url, domain, username, password):
        self.domain = domain
        self.username = username
        self.password = password
        self.url = url
        self.session = requests.Session()
        self.request = None
        self.authentication = HttpNtlmAuth(("%s\\%s" % (self.domain,
                                                        self.username)),
                                                        self.password)
        self.headers = {'accept': 'application/json;odata=verbose'}
        self.request_page(self.url)

    def request_page(self, url):
        relative_url = urljoin(self.url, url)
        print(relative_url)
        self.request = self.session.get(relative_url,
                                        auth=self.authentication,
                                        headers=self.headers)
        return self.request

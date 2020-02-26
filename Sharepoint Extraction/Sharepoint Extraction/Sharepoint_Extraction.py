import argparse
import urllib.parse
import os
import requests
from requests_ntlm3 import HttpNtlmAuth

API_GETFILEURI = "_api/Web/GetFileByServerRelativeUrl('/"
API_GETFOLDERURI = "_api/Web/GetFolderByServerRelativeUrl('/"

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--server', default="http://sharepoint")
PARSER.add_argument('-u', '--username', required=True)
PARSER.add_argument('-p', '--password', required=True)
ARGS = PARSER.parse_args()
SERVER = urllib.parse.urljoin(ARGS.server, '/')

AUTH = HttpNtlmAuth(ARGS.username, ARGS.password)
HEADERS = {'accept': 'application/json;odata=verbose'}

def make_request(url):
    response = requests.get(url, auth=AUTH, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def download_file(filename):
    filename = filename.strip('/')
    print('Downloading\t'+filename)
    response = requests.get(SERVER+API_GETFILEURI+filename+"')/$value", auth=AUTH, stream=True)
    with open(filename, 'wb+') as f_stream:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f_stream.write(chunk)
                f_stream.flush()

def check_directory(path):
    path = path.strip('/')
    print('Checking\t'+path)
    os.makedirs(path, exist_ok=True)
    response = make_request(SERVER+API_GETFOLDERURI+path+"')/Folders")
    if response is not None:
        folders = response['d']['results']
        for folder in folders:
            check_directory(folder['ServerRelativeUrl'])
    response = make_request(SERVER+API_GETFOLDERURI+path+"')/Files")
    if response is not None:
        files = response['d']['results']
        for file in files:
            download_file(file['ServerRelativeUrl'])

check_directory('/Shared Documents')

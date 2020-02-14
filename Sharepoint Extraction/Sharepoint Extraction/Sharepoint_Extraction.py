import argparse
import urllib.parse
import os
import requests
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser()
parser.add_argument('server')
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()
server = urllib.parse.urljoin(args.server,'/')

auth = HTTPBasicAuth(args.username, args.password)
headers = {'accept': 'application/json;odata=verbose'}

def make_request(url):
    r = requests.get(url, auth=auth, headers=headers)
    return r.json()

def download_file(filename):
    filename = filename.strip('/')
    print('Downloading\t'+filename)
    r = requests.get(server+"_api/Web/GetFileByServerRelativeUrl('/"+filename+"')/$value", auth=auth, stream=True)
    with open(filename, 'wb+') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
                f.flush()

def check_directory(path):
    path = path.strip('/')
    print('Checking\t'+path)
    if not os.path.exists(path):
        os.makedirs(path)
    folders = make_request(server+"_api/Web/GetFolderByServerRelativeUrl('/"+path+"')/Folders")['d']['results']
    for folder in folders:
        check_directory(folder['ServerRelativeUrl'])
    files = make_request(server+"_api/Web/GetFolderByServerRelativeUrl('/"+path+"')/Files")['d']['results']
    for file in files:
        download_file(file['ServerRelativeUrl'])

check_directory('/Shared Documents')
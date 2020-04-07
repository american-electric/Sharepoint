from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import urllib.request
import urllib
import os
import re
import json
from pathlib import Path
import sys
import getopt
import shutil

sharepointUri = 'http://sharepoint'
baseUri = urllib.parse.urljoin(sharepointUri,'operations/solar/Shared%20Documents/Forms/AllItems.aspx')
basicAuth = HTTPBasicAuth('HSI\\ajans','cH3wyM0ck!ngb!rd')
dlRoot = 'C:/TEMP'

try:
  opts, args = getopt.getopt(sys.argv[1:],"hu:d:",["url=","dest="])
except getopt.GetoptError:
  print('sharepoint_webscraping.py -u <url> -d <destpath>')
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
     print('sharepoint_webscraping.py -u <url> -d <destpath>')
     sys.exit()
  elif opt in ("-u", "--url"):
     baseUri = arg
  elif opt in ("-d", "--dest"):
     dlRoot = arg

def download_file(url_path, basic_auth):
    filename = os.path.join(dlRoot, urllib.parse.unquote(url_path))
    print(filename)
    os.makedirs(filename.replace(filename.split('/')[-1],''), exist_ok=True)
    if not os.path.isfile(filename):
        with requests.get(urllib.parse.urljoin(sharepointUri, url_path), auth=basic_auth, stream=True) as r:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.content,f)
                print("Download Complete!")

def download_folder(url_path, basic_auth):
    source = requests.get(url_path, auth=basicAuth).text
    soup = BeautifulSoup(source, 'lxml')
    for docLink in soup.find_all('a', onfocus="OnLink(this)", href=True):
        href = docLink.get('href')
        try:
            print(urllib.parse.unquote(href))
            if 'AllItems.aspx' in href:
                download_folder(href, basic_auth)
            else:
                download_file(href, basic_auth)
        except:
            print(href, file=sys.stderr)
    next = soup.find('img', alt='Next')
    if next is not None:
        nextLink = next.find_parent('a')
        link = re.search('"(.*)"',nextLink.get('onclick'))
        download_folder(json.loads(link.group()),basic_auth)

download_folder(baseUri, basicAuth)
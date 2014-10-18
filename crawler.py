from bs4 import BeautifulSoup
import urllib
import re
from urllib.parse import urljoin

base_url = "http://cs61a.org"

response = urllib.request.urlopen(url)
page = BeautifulSoup(response)

table = page.find('table', id='calendar')
for a in table.find_all('a'):
    # Homework Fetch
    if 'homework' in a.string.lower():
        print(a.string, end=': ')
        td = a.parent
        link = td.find('a', text=re.compile('hw'))
        file_link = link.get('href')
        full_link = urljoin(base_url, file_link)
        print(full_link)

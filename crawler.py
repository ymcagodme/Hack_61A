import re
import urllib.request
import sys

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.error import *

base_url = "http://cs61a.org"

def full_link(relative_link):
    if base_url in relative_link:
        return relative_link
    return urljoin(base_url, relative_link)


response = urllib.request.urlopen(base_url)
page = BeautifulSoup(response)

table = page.find('table', id='calendar')

hw_pattern = 'hw\d+\.py'
lab_pattern = 'lab\d+\.py'
lab_extra_pattern = 'lab\d+_extra\.py'
proj_pattern = '\S+\.zip'

hw_paths = {}
lab_paths = {}
proj_paths = {}

lab_pages = []
proj_pages = []

links = table.find_all('a')
for link in links:
    href = link.get('href')

    # Fetch Homework
    if re.search(hw_pattern, href):
        name = link.string.replace(".py", "")
        paths = hw_paths.get(name, [])
        paths.append(full_link(href))
        hw_paths[name] = set(paths)

    # Fetch Lab Pages
    if re.search('lab', href):
        lab_pages.append(full_link(href))

    # Fetch Project Pages
    if re.search('proj', href):
        proj_pages.append(full_link(href))

for url in proj_pages:
    response = urllib.request.urlopen(url)
    page = BeautifulSoup(response)
    links = page.find_all('a')
    title = page.title.string.lower()
    match = re.search('project \d+:', title)
    if match is None:
        match = re.search('.+\:', title)
        s = match.start()
        e = match.end()
        name = title[s:e-1]
    else:
        s = match.start()
        e = match.end()
        number = (title[s:e-1]).replace("project ", "")
        name = 'proj' + number
    files = []

    for l in links:
        href = l.get('href')
        if re.search(proj_pattern, href):
            files.append(full_link(href))
    files = set(files)
    proj_paths[name] = files

if 0:
    print("Fetching lab...")
    for url in lab_pages:
        response = urllib.request.urlopen(url)
        page = BeautifulSoup(response)
        links = page.find_all('a')

        title = page.title.string.lower()
        match = re.search('lab \d+:', title)
        if match is None:
            match = re.search('.+\:', title)
            s = match.start()
            e = match.end()
            name = title[s:e-1]
        else:
            s = match.start()
            e = match.end()
            number = (title[s:e-1]).replace("lab ", "")
            name = 'lab' + number
        files = []
        for link in links:
            href = link.get('href')
            if re.search(lab_pattern, href):
                files.append(full_link(href))
            # TODO: Fetch the lab_extra files
            if re.search(lab_extra_pattern, href):
                files.append(full_link(href))
        files = set(files)
        lab_paths[name] = files

hw_paths = {'hw5': {'http://cs61a.org/hw/released/hw5.py'},
         'hw3': {'http://cs61a.org/hw/released/hw3.py'},
          'hw6': {'http://cs61a.org/hw/released/hw6.py'},
           'hw1': {'http://cs61a.org/hw/released/hw1.py'},
            'hw2': {'http://cs61a.org/hw/released/hw2.py'},
             'hw4': {'http://cs61a.org/hw/released/hw4.py'}}

from server import db
from server import Assignment
from server import Link

for name, links in hw_paths.items():
    hw = Assignment('hw', name)
    for link in links:
        l = Link(link, hw)
        db.session.add(l)
    db.session.add(hw)

# for name, links in lab_paths.items():
#     lab = Assignment('lab', name)
#     for link in links:
#         l = Link(l, lab)
#         db.session.add(l)
#     db.session.add(hw)

# for name, links in proj_paths.items():
#     proj = Assignment('proj', name)
#     for link in links:
#         l = Link(l, proj)
#         db.session.add(l)
#     db.session.add(proj)

db.session.commit()

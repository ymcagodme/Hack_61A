#! /usr/bin/env python
import sys, os, argparse
import urllib.request
from subprocess import call
import json as m_json

parser = argparse.ArgumentParser(prog='hws')
parser.add_argument('init', nargs='+', help='homework, lab, project name, ex:hw1')

args = parser.parse_args()
dict_args = vars(args)
args_list = dict_args['init']
base_url = "http://127.0.0.1:5000/"

def init_option(work_name):
    print("init", work_name)
    path = work_name
    try:
        os.makedirs(path)
        hw_response = urllib.request.urlopen(base_url + "hws/").read()
        lab_response = urllib.request.urlopen(base_url + "labs/").read()
        proj_response = urllib.request.urlopen(base_url + "projs/").read()
        print(hw_response)
        print(hw_response.decode('utf8'))
        hw_json = m_json.loads(hw_response.decode('utf8'))
        lab_json = m_json.loads(lab_response.decode('utf8'))
        proj_json = m_json.loads(proj_response.decode('utf8'))
        if (work_name in hw_json):
            file_url_lst = hw_json[work_name]
        elif (work_name in lab_json):
            file_url_lst = lab_json[work_name]
        elif (work_name in proj_json):
            file_url_lst = proj_json[work_name]
        print(type(file_url_lst))
        print(file_url_lst)
        # for link in list(file_url_lst):
        #     print(link)
            # args = "-P"
            # folder_name = work_name + "/"
            # call(['wget', args, folder_name, link])
            # file_name = path + "/"
            # code = urllib.request.urlopen(links).read()
            # f = open(file_name, "a")
            # f.write(code.decode('utf8'))
            # f.close()
    except OSError as exception:
        print("exists " + work_name + " folder")

def version_option():
    print("version option")

def list_option():
    hw_response = urllib.request.urlopen(base_url + "hws/").read()
    lab_response = urllib.request.urlopen(base_url + "labs/").read()
    proj_response = urllib.request.urlopen(base_url + "projs/").read()
    hw_json = m_json.loads(hw_response.decode('utf8'))
    lab_json = m_json.loads(lab_response.decode('utf8'))
    proj_json = m_json.loads(proj_response.decode('utf8'))
    hw_list = []
    lab_list = []
    proj_list = []
    for item in sorted(hw_json):
        hw_list.append(item)
    for item in sorted(lab_json):
        lab_list.append(item)
    for item in sorted(proj_json):
        proj_list.append(item)
    total = len(hw_list) + len(lab_list) + len(proj_list)
    print("Available assignments ({0})".format(total))
    print('-----------------------------')
    print("===== Homeworks ({0}) =====".format(len(hw_list)))
    for hw in hw_list:
        print(" - " + hw)
    print()
    print("===== Labs ({0}) =====".format(len(lab_list)))
    for lab in lab_list:
        print(" - " + lab)
    print()
    print("===== Projects ({0}) =====".format(len(proj_list)))
    for proj in proj_list:
        print(" - " + proj)
    print()

def sync_option():

    print("sync option")

func_name = args_list[0]

if func_name == 'init':
    if len(args_list) < 2:
        print("Insufficient Arguments")
        parser.print_help()
        sys.exit()
    init_option(args_list[1])
elif func_name == 'version':
    version_option(args_list[1])
elif func_name == 'list':
    list_option()
elif func_name == 'sync':
    sync_option()


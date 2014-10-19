#! /usr/bin/env python
import sys, os, argparse
import urllib.request
from subprocess import call
import json as m_json

parser = argparse.ArgumentParser(prog='hws')
parser.add_argument('init', nargs='+', help='[assingment name]')
parser.add_argument('list', nargs='+', help='List all available assignments')

args = parser.parse_args()
dict_args = vars(args)
args_list = dict_args['init']
base_url = "http://127.0.0.1:5000/"

def init_option():
    path = "cs61a"
    try:
        os.makedirs(path)
        os.makedirs(path + "/hw")
        os.makedirs(path + "/lab")
        os.makedirs(path + "/proj")
    except OSError as exception:
        print("Exists " + path + " Folder")
    print("Initialized CS61A Working Folder")

def init_work_option(work_name):
    print("Initializing", work_name)
    try:
        hw_response = urllib.request.urlopen(base_url + "hws/").read()
        lab_response = urllib.request.urlopen(base_url + "labs/").read()
        proj_response = urllib.request.urlopen(base_url + "projs/").read()
        hw_json = m_json.loads(hw_response.decode('utf8'))
        lab_json = m_json.loads(lab_response.decode('utf8'))
        proj_json = m_json.loads(proj_response.decode('utf8'))
        work_folder_name = ""
        if (work_name in hw_json):
            file_url_lst = hw_json[work_name]
            # work_folder_name = "hw/"
        elif (work_name in lab_json):
            file_url_lst = lab_json[work_name]
            # work_folder_name = "lab/"
        elif (work_name in proj_json):
            file_url_lst = proj_json[work_name]
            # work_folder_name = "proj/"
        path = work_folder_name + work_name
        os.makedirs(path)
        for link in file_url_lst:
            folder_arg = "-P"
            folder_name = path + "/"
            quiet_arg = "-q"
            call(['wget', quiet_arg, folder_arg, folder_name, link])
            # file_name = path + "/"
            # code = urllib.request.urlopen(links).read()
            # f = open(file_name, "a")
            # f.write(code.decode('utf8'))
            # f.close()
        print("Downloaded",len(file_url_lst),"files")
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

# def sync_option():
    # login = input("Login(cs61a-xx): ")
    # login_string = login + "@torus.cs.berkeley.edu"
    # cur_path = os.getcwd()
    # lst = cur_path.split('/')
    # index = 0
    # remote_path = "~/"
    # for i in range(len(lst)):
    #     if lst[i] == 'cs61a':
    #         index = i
    #         break
    # for i in range(index, len(lst)):
    #     remote_path += lst[i] + "/"
    #     call(['ssh', login_string, "mkdir " + remote_path])
    # call(['scp', '*', login_string + ":~" + remote_path])
    # print("Sync option")

func_name = args_list[0]

if func_name == 'init':
    if len(args_list) == 2:
    #     print("Insufficient Arguments")
    #     parser.print_help()
    #     sys.exit()
        init_work_option(args_list[1])
    else:
        init_option()
elif func_name == 'version':
    version_option(args_list[1])
elif func_name == 'list':
    list_option()
elif func_name == 'sync':
    sync_option()


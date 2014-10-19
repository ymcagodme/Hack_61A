#! /usr/bin/env python
import sys, os, argparse

parser = argparse.ArgumentParser(prog='hws')
parser.add_argument('init', nargs='+', help='homework, lab, project name, ex:hw1')

args = parser.parse_args()
dict_args = vars(args)
args_list = dict_args['init']

def init_option(work_name):
    print("init", work_name)
    path = work_name
    try:
        os.makedirs(path)
        open(work_name + "/" + work_name + ".py", "a").close()
    except OSError as exception:
        print("exists " + work_name + " folder")

def version_option():
    print("version option")

def list_option():
    print("list option")

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


import os
import time
import shutil
import json
import datetime
import random
import re


def new_file_name(start_str='',end_str=''):
    return str(start_str)+str(time.time())+'-'+str(random.random())+str(end_str)


def makedirs_if_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(path , 'is exists')
    return path


def write_text_file(data,path_url='./text'):
    f=open(path_url,"w",encoding='utf-8')
    f.truncate()
    f.write(data)
    f.close()


def new_time(g="%Y-%m-%d-%I-%M-%S-"):
    return time.strftime(g, time.localtime())



def all_remove_dir(path_dir):
    path_dir_conf = path_dir
    if re.search(r'[/\\]$',path_dir):
        path_dir_conf = path_dir[0:len(path_dir)-1]
    makedirs_if_exists(path_dir_conf)
    shutil.rmtree(path_dir_conf)
    makedirs_if_exists(path_dir_conf)


def save_json(agg,path):
    if len(agg):
        if not re.search(r'[/\\]$',path):
            path+='/'
        write_text_file(json.dumps(agg), path+new_file_name())


def save_text_logs(text,path,end_str):
    if len(text):
        if not re.search(r'[.\\]$',path):
            path+='/'
        write_text_file(text,path+new_file_name('logs','.netelf_logs'+str(end_str)))
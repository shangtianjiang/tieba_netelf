import os
import re


server_database_url = 'http://127.0.0.1:8880/2020/tieba_netelf_web/view_logic/open.php?a=push_data'
set_data = {}
start_str='~'
link_str='='


def from_file_read_conf():
    conf_path='./netelf_tieba.ini'
    if os.path.exists(conf_path):
        conf_file=open(conf_path,'r+')
        conf_data=conf_file.read(-1)
        conf_file.close()
        str_r=f"{start_str}([^=\n]*){link_str}([^\n]*)"
        data=re.findall(str_r,conf_data)
        for value in data:
            try:
                i_=value[0]
                v_=value[1]
                set_data[i_]=v_
            except Exception as e:
                print("Error_from_file_read_conf : ", e)
    else:
        print('./netelf_tieba.ini is null - Please create a file or update the latest profile')


def read_conf(index_name,d=None):
    try:
        return set_data[index_name]
    except Exception as e:
        return d

def data_struct(
        yid,
        username,
        img,
        text,
        tieba_name,
        post_name,
        tid
    ):
    return {
        'yid':str(yid),
        'username':username,
        'img':img,
        'text':text,
        'tieba_name':tieba_name,
        'post_name':post_name,
        'tid':tid
    }


def post_struct(tid,tieba_name,data_name):
    return {
        'tid':tid,
        'tieba_name':tieba_name,
        'post_name':data_name,
    }

from_file_read_conf()







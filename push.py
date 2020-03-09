import os
import json
import net
import conf
import re
def push_dir_file(path):
    if not re.search(r'[/\\]$', path):
        path += '/'
    dir=path
    data=[]
    url=conf.read_conf('website_push_data_url','http://127.0.0.1')
    file_agg=list(os.walk(dir))[0][2]
    for file_name in file_agg:
        file_path=dir+file_name
        file=open(file_path,"r")
        json_string=file.read(-1)
        data.append({
            'url':url,
            'data':{
                'tiebaUserMsgJsonStr':json_string
            }
        })
        if len(data)!=0 and not len(data)%3:
            re_net=net.post_text_agg(data)
            print(re_net)
            data.clear()

if __name__ == '__main__':
    push_dir_file(conf.read_conf('netelf_cache','./netelf_cache'))
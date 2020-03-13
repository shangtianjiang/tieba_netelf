import os
import json
import net
import conf
import re
import errorClass
def push_dir_file(path):
    try:
        if not re.search(r'[/\\]$', path):
            path += '/'
        dir=path
        data=[]
        url=conf.read_conf('website_push_data_url','http://127.0.0.1')
        file_agg=list(os.walk(dir))[0][2]
        for file_name in file_agg:
            try:
                file_path=dir+file_name
                file=open(file_path,"r")
                json_string=file.read(-1)
                data.append({
                    'url':url,
                    'data':{
                        'tiebaUserMsgJsonStr':json_string
                    }
                })
                if len(data)!=0 and not len(data) % int(conf.read_conf('syn_push_data_num',4)):
                    re_net=net.post_text_agg(data)
                    print(re_net)
                    data.clear()
            except Exception as e:
                errorClass.new_error_log('push_dir_file_for_Error: ',e,'error')
        if len(data)>0:
            re_net = net.post_text_agg(data)
            print(re_net)
            data.clear()
    except Exception as e:
        errorClass.new_error_log('Error_push_dir_file_Error: ',e,'error')

if __name__ == '__main__':
    push_dir_file(conf.read_conf('netelf_cache','./netelf_cache'))
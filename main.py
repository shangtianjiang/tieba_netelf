# import asyncio
# import http3
# async def t():
#     client = http3.AsyncClient()
#     r = await client.get('https://tieba.baidu.com/')
#
#
# async def main():
#     await asyncio.gather(
#         t()
#     )
#
#
# asyncio.run(t())



# import requests
import json

# import asyncio
# import aiohttp
# from userAgent import new_user_agent
from net import get_text_streamed
from dataAbstract import *
import conf
from file import *
import push
import time


def new_home_url(kw,pn):
    return f'https://tieba.baidu.com/f?ie=utf-8&kw={kw}&pn={pn}'



def new_comment_url(tid,pn):
    return f'https://tieba.baidu.com/p/totalComment?tid={tid}&pn={pn}'



def new_post_url(tid,pn):
    return f'https://tieba.baidu.com/p/{tid}?pn={pn}'


def post_agg_url(posts_agg_source):
    for posts_i in range(0, len(posts_agg_source)):
        try:
            # from post pn 2 so post_pn
            post_pn = 1
            post_home = posts_agg_source[posts_i]
            post_data_agg = []
            post_info = from_page_get_pageInfo(post_home)
            post_tid = post_info["tid"]
            post_pn_max = from_home_get_postMax(post_home, post_tid)
            post_agg = [post_home]
            post_agg_next = [new_post_url(post_tid, post_pn) for post_pn in range(post_pn + 1, post_pn_max + 1)]
            post_agg += get_text_streamed(post_agg_next)
            for post_i in range(0, len(post_agg)):
                try:
                    post_data_agg += from_page_get_postsData(post_agg[post_i], post_info)
                except Exception as e:
                    print("Error_post_agg_url_1 : ", e)
                if post_i != 0 and post_i % 40 == 0:
                    save_json(post_data_agg, conf.read_conf('netelf_cache','./netelf_cache'))
                    post_data_agg = []
            save_json(post_data_agg, conf.read_conf('netelf_cache','./netelf_cache'))
            post_data_agg = []
            # get comment
            get_comment_url_agg = [new_comment_url(post_tid, comment_pn) for comment_pn in range(1, post_pn_max + 1)]
            comment_agg = get_text_streamed(get_comment_url_agg)
            for comment_i in range(0, len(comment_agg)):
                try:
                    post_data_agg += from_jsonComment_get_pageData(comment_agg[comment_i], post_info)
                except Exception as e:
                    print("Error_post_agg_url_2 : ", e)
                if comment_i != 0 and comment_i % 40 == 0:
                    save_json(post_data_agg, conf.read_conf('netelf_cache','./netelf_cache'))
                    post_data_agg = []
            save_json(post_data_agg, conf.read_conf('netelf_cache','./netelf_cache'))
        except Exception as e:
            print("Error_post_agg_url_3 : ", e)





def main():
    ba_agg = []
    try:
        print('target_part_source', conf.read_conf('website_get_target_part'))
        target_part = json.loads(
            get_text_streamed([conf.read_conf('website_get_target_part')])[0]
                                 )
        if target_part['code'] == 200:
            ba_agg=target_part['data']
        else:
            print('target_part_code is ', target_part, ' request ')
    except Exception as e:
        print('target_part_Error: ', e)
    print('target_agg: ',ba_agg)
    posts_agg = []
    for ba_i in range(0, len(ba_agg)):
        home_agg = get_text_streamed([new_home_url(ba_agg[ba_i], 0) ])
        for home_i in range(0, len(home_agg)):
            all_remove_dir(conf.read_conf('netelf_cache','./netelf_cache')) #clear
            pn_num_max_conf=350*50
            home_content_code = from_home_get_content(home_agg[home_i])
            posts_agg += from_text_get_posts(home_content_code)
            pn_num_max = from_home_get_homeMax(home_content_code)
            pn_num_start = 1*50
            pn_num_now = 100*50
            while pn_num_start < pn_num_max:
                pn_num_end=pn_num_start+pn_num_now
                get_list_url_agg = [new_home_url(ba_agg[home_i], pn_num_i) for pn_num_i in range(pn_num_start,min( pn_num_max + 50,pn_num_end),50)]
                get_list_agg = get_text_streamed(get_list_url_agg)
                for list_i in range(0, len(get_list_agg)):
                    data=from_home_get_content(get_list_agg[list_i])
                    posts_agg += from_text_get_posts(data)
                del get_list_agg
                del get_list_url_agg
                posts_agg=list(set(posts_agg))
                posts_agg_start = 0
                posts_agg_now = 100
                while posts_agg_start < len(posts_agg):
                    posts_agg_end=posts_agg_start+posts_agg_now
                    #get post 1
                    posts_agg_source=get_text_streamed([new_post_url(posts_agg[posts_i],1) for posts_i in range(posts_agg_start,min(len(posts_agg),posts_agg_end) )])
                    post_agg_url(posts_agg_source)
                    # posts_start next
                    posts_agg_start = posts_agg_end
                pn_num_start=pn_num_end
        push.push_dir_file(conf.read_conf('netelf_cache','./netelf_cache'))

while True:
    print('Run main ~')
    main()
    print('-'*20)
    print('Sleep 10800 s')
    time.sleep(60*60*3)

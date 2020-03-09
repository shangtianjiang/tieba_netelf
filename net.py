import requests
import json
import time
from lxml import etree
import re
import asyncio
import aiohttp
from userAgent import new_user_agent


async def get_text(url):
    async with aiohttp.ClientSession() as session:
        state=0
        while state != 200:
            async with session.get(url, headers={'User-Agent':new_user_agent()}) as response:
                state = response.status
                if state == 200:
                    return {'data': await response.text("utf-8","ignore"),'state':response.status}


async def post_text(url,post_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers={'User-Agent':new_user_agent()},data=post_data) as response:
            return {'data': await response.text("utf-8","ignore"),'state':response.status}


def post_text_agg(url_agg):
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(len(url_agg)):
        task = asyncio.ensure_future(post_text(url_agg[i]["url"],url_agg[i]["data"]))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    return result


def get_text_agg(url_agg):
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(len(url_agg)):
        task = asyncio.ensure_future(get_text(url_agg[i]))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    print('Success net url: ',url_agg)
    return result



def get_text_streamed(_url_agg,get_max=50,start=0):
    streamed_start = start
    return_agg = []
    url_agg= _url_agg.copy()
    while streamed_start != len(url_agg):
        streamed_end = min(streamed_start+get_max , len(url_agg))
        try:
            get_data=(get_text_agg(url_agg[streamed_start : streamed_end ]))
            for data_i in range(0,len(get_data)):
                if get_data[data_i]['state'] == 200:
                    return_agg.append(get_data[data_i]['data'])
                elif get_data[data_i]['state'] == 403:
                    url_agg.append(url_agg[streamed_start+data_i])
                else:
                    print('Warning: net url: ',url_agg[streamed_start+data_i],' state: ',url_agg[streamed_start+data_i]['state'])
            streamed_start = streamed_end
        except Exception as e:
            print("Error_get_text_streamed: ",e)

    return return_agg


import re
from lxml import etree
import conf
import json
import errorClass


re_get_posts = re.compile(r'href="/p/([0-9]+)"')


re_get_homeMax = re.compile(r'&pn=([0-9]+)"')


def xpath_try(obj,xpath_str,de):
    x_data=obj.xpath(xpath_str)
    if x_data is None or len(x_data) == 0:
        return de
    else:
        return x_data




def from_home_get_content(text, decode='utf-8'):
    try:
        html = etree.HTML(text)
        return html.xpath('//*[@id="pagelet_html_frs-list/pagelet/thread_list"]/node()')[0].text
    except Exception as e:
        errorClass.new_error_log('from_home_get_content: ',e,'error')
        return ''



def from_text_get_posts(text):
    return re_get_posts.findall(text)



def from_home_get_homeMax(text):
    try:
        pn_agg = re_get_homeMax.findall(text)
        return  int(pn_agg[len(pn_agg)-1])
    except Exception as e:
        errorClass.new_error_log('from_home_get_homeMaxError: ',e,'error')
        return 0


def from_home_get_postMax(text, tid):
    re_str = f'<a href="/p/{tid}\?pn=([0-9]+)">'
    re_get_post_max = re.compile(re_str)
    pn_agg = re_get_post_max.findall(text)
    if(len(pn_agg)):
        return int(pn_agg[len(pn_agg) - 1])
    else:
        return 0



def from_page_get_postsData(text, postInfo):
    return_agg=[]
    html=etree.HTML(text,etree.HTMLParser(encoding='gbk'))
    block_content=html.xpath('//div[@id="j_p_postlist"]/div')
    for bci in range(0,len(block_content)):
        try:
            posts_content = block_content[bci]
            post_html = etree.HTML(etree.tostring(posts_content))
            yid=xpath_try(post_html,'//cc/div[contains(@id,"post_content_")]/@id',[''])[0]
            if yid == '':
                raise errorClass.no_data('')
            username=xpath_try(post_html,'//img/@username', [''])[0]
            data_content_text=xpath_try(post_html, '//cc/div[contains(@id,"post_content_")]', [''])[0]
            data_content=etree.HTML(etree.tostring(data_content_text) , etree.HTMLParser() )
            data_text=data_content.xpath('//text()')
            return_text=''
            for d_t_i in range(0,len(data_text)):
                return_text+=data_text[d_t_i]
            data_img=data_content.xpath('//img/@src')
            data_s=conf.data_struct(
                yid=yid,
                username=username,
                img=data_img,
                text=''.join(data_text),
                tieba_name=postInfo['tieba_name'],
                post_name=postInfo['post_name'],
                tid=postInfo['tid']
            )
            data_s.update(postInfo)
            return_agg.append(data_s)
        except errorClass.no_data as e:
            print('yid is null '+e.val)
        except Exception as e:
            errorClass.new_error_log('Error_from_page_get_postsData: ',e,'error')
    return return_agg



def from_page_get_pageInfo(text):
    tieba_name=re.search(r'fname="([^"]*)"', text)
    tid=re.search(r'<link rel="canonical" href="//tieba\.baidu\.com/p/([^"]*)"/>', text)
    post_name=re.search(r'<h[0-9] class="core_title_txt[\S\s]+?title="([^"]*)"', text)
    if tid is None:
        print('tid is None')
    else:
        print('tid: ',tid[1])
    return conf.post_struct('' if tid is None else tid[1],
                             '' if tieba_name is None else tieba_name[1],
                             '' if post_name is None else post_name[1],)



def from_jsonComment_get_pageData(jsonString, postInfo ):
    return_agg = []
    try:
        comment_data = json.loads(jsonString)
        comment_list = comment_data['data']['comment_list']
        if (len(comment_list)):
            data_agg=list(comment_list.values())
            for data_i in  range(0,len(data_agg)):
                data_p=data_agg[data_i]['comment_info'][0]
                yid=data_p['comment_id']
                content=data_p['content']
                img_url=re.findall(r'src="([^"]*)"',data_p['content'])
                user_id=data_p['user_id']
                data_s=conf.data_struct(
                    yid=yid,
                    text=content,
                    img=img_url,
                    username=user_id,
                    tieba_name=postInfo['tieba_name'],
                    post_name=postInfo['post_name'],
                    tid=postInfo['tid']
                )
                return_agg.append(data_s)
    except Exception as e:
        errorClass.new_error_log('Error_from_jsonComment_get_pageData: ',e,'error')
    return return_agg

# 5720985210
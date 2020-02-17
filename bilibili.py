# -*- coding: utf-8 -*-
"""
File Name：     bilibili
Description :
Author :       meng_zhihao
mail :       312141830@qq.com
date：          2019/7/25
"""
import datetime
from crawl_tool_for_py3 import crawlerTool as ct
import time
import json
import csv

def get_author_info(mid):
    author_url = 'https://space.bilibili.com/%s?spm_id_from=333.788.b_765f7570696e666f.2'%mid
    # views_info_url = 'https://api.bilibili.com/x/space/upstat?mid=%s&jsonp=jsonp&callback=__jp4'%mid
    author_info_url ='https://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp'%mid #sex
    author_info = ct.get(author_info_url).decode('utf8')
    author_info = json.loads(author_info)
    sex = author_info.get('data',{}).get('sex')
    return sex

def get_video_info(aid):
    info_url = 'https://api.bilibili.com/x/web-interface/view?aid=%s&cid=104953812'%aid
    video_info = ct.get(info_url)
    video_info = json.loads(video_info)
    stat = video_info.get('data').get('stat')
    coin = stat['coin'] # 硬币
    like = stat['like'] # 点赞
    share = stat['share'] # 转发
    favorite = stat['favorite'] # 收藏
    reply = stat['reply']  # 评论
    return coin,like,share,favorite,reply

if __name__ == "__main__":
    end_date  = datetime.datetime.now().strftime("%Y%m%d")
    start_date = (datetime.datetime.now()-datetime.timedelta(7)).strftime("%Y%m%d")
    time_stamp = int(time.time()*1000)
    video_infos = {}

    print(start_date,end_date)
    fout = open('result%s.csv'%end_date, 'w', newline='')
    csv_writer = csv.writer(fout)
    csv_writer.writerow(['video_id','title','author','author_gender','view_count','danmu_count','coin_count',
                         'pubdate','favorite_count','like_count','share_count','reply'])
    for page_no in range(1,1000,1):
        try: # cate_id=157对应美妆
            start_url = 'https://s.search.bilibili.com/cate/search?callback=&main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=157&page=%s&pagesize=20&jsonp=jsonp&time_from=%s&time_to=%s&_=%s'%(page_no,start_date,end_date,time_stamp)
            print(start_url)
            page_buf = ct.get(start_url).decode('utf8')
            print(page_buf)
            json_str = ct.getRegex('(\{.*\})',page_buf)
            values = json.loads(json_str)
            video_results = values['result']
            for video_result in video_results:
                video_id = video_result['id']
                pubdate = video_result['pubdate'] # 发布日期
                play = video_result['play'] # 播放量
                title = video_result['title'] # 标题
                video_review = video_result['video_review'] # 弹幕数
                duration = video_result['duration'] # 时长
                author_id = video_result['mid'] # 作者id
                author = video_result['author'] # 作者名
                print(title)
                try:
                    sex = get_author_info(author_id)
                except Exception as e:
                    sex = ''
                    print(e)
                try:
                    coin, like, share, favorite,reply = get_video_info(video_id)
                except Exception as e:
                    coin, like, share, favorite,reply = '','','','',''
                    print(e)
                csv_writer.writerow([video_id,title,author,sex,play,video_review,coin,pubdate,favorite,like,share,reply])
                fout.flush() # 中途保存
            max_page = int(values['numPages'])
            if page_no >= max_page:
                break
        except Exception as e:
            print(e)


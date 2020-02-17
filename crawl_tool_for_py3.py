# -*- coding: utf-8 -*-
"""
File Name：     crawl_tool_for_py3
Description :
Author :       meng_zhihao
date：          2018/11/20

"""

import requests
from lxml import etree
import re
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

#通用方法
class crawlerTool:

    def __init__(self):
        self.session = requests.session()
        pass

    def __del__(self):
        self.session.close()

    @staticmethod
    def get(url,proxies=None):
        rsp = requests.get(url,timeout=10,proxies=proxies)
        return rsp.content # 二进制返回

    @staticmethod
    def post(url,data):
        rsp = requests.post(url,data,timeout=10)
        return rsp.content


    def sget(self,url,cookies={}):
        rsp = self.session.get(url,timeout=10,headers=HEADERS,cookies=cookies)
        return rsp.content # 二进制返回

    def spost(self,url,data):
        rsp = self.session.post(url,data,timeout=10,headers=HEADERS)
        return rsp.content



    # 获取xpath 要判断一下输入类型，或者异常处理
    @staticmethod
    def getXpath(xpath, content):   #xptah操作貌似会把中文变成转码&#xxxx;  /text()变unicode编码
        """

        :param xpath:
        :param content:
        :return:
        """
        tree = etree.HTML(content)
        out = []
        results = tree.xpath(xpath)
        for result in results:
            if  'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)) :
                out.append(result)
            else:
                out.append(etree.tostring(result,encoding = "utf8",method = "html"))
        return out

    @staticmethod
    def getRegex(regex, content):
        rs = re.search(regex,content)
        if rs:
            return rs.group(1)
        else:
            return ''


if __name__ == '__main__':
    content = (crawlerTool.get('https://www.chemicalbook.com/ShowSupplierProductsList684/0.htm'))
    content = (content.decode('utf8'))
    print(crawlerTool.getXpath('//tr/td[2]/text()',content))

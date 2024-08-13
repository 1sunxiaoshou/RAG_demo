import re
import csv
import requests
from bs4 import BeautifulSoup


def get_baidu_baike_content(keyword):
    url = f"https://baike.baidu.com/item/{keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        # 获取标题
        title = soup.find('h1').get_text(strip=True)
        content = soup.find('meta', attrs={'name': 'description'}).get('content')
        # 使用正则表达式进行匹配
        link_node = soup.find('div', attrs={'class':re.compile(r"basicInfo_")})

        info_dict = {}

        for i in link_node:
            for j in i:
                key = re.sub(r'\s+', '', j.dt.get_text(strip=True))
                value = re.sub(r'\[\d+\]', '', j.dd.get_text(strip=True))
                info_dict[key]=value

        result = {'标题':title,'简介': content,'属性':info_dict}

        return result
    else:
        return "页面获取失败"

def sava_data(key_list:list,csv_path:str):
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入标题行
        writer.writerow(['标题','简介','属性'])
        for key in key_list:
            result = get_baidu_baike_content(key)
            writer.writerow(result.values())

# 示例使用
nouns = ['米哈游', '腾讯', '阿里巴巴', '苹果', '微软', '谷歌', '华为', '小米', '联想', '百度', '字节跳动', '网易', '京东', '拼多多', '美团', '滴滴出行', '蚂蚁金服', '哔哩哔哩', '新浪', '搜狐', '优酷', '爱奇艺', '知乎', '豆瓣', '小红书', '微信', '支付宝', '抖音', '快手', '微博', '淘宝', '天猫', '京东商城', '苏宁易购', '国美电器', '唯品会', '当当网', '亚马逊中国']
csv_path = 'output.csv'
sava_data(nouns,csv_path)

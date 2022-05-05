# -*- coding:utf-8 -*-
# @Time : 2022/4/20 19:06
# @File : test.py
# @Software : PyCharm
import time

import requests
import re
import os

CAPTCHA_IMAGE_FOLDER = "/Users/mason/PycharmProjects/typoraCracker/auto-analysis/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

if not os.path.exists(CAPTCHA_IMAGE_FOLDER):  # 如果不存在目标文件夹，则重新建立该文件夹
    os.makedirs(CAPTCHA_IMAGE_FOLDER)

page = 0
while page <= 225:
    res = requests.get('https://movie.douban.com/top250?start=' + str(page) + '&filter=', headers=headers)
    html = res.text
    chapter_photo_list = re.findall(r'https:.*jpg', html)

    m = 1
    for chapter_photo in chapter_photo_list:
        img = requests.get(chapter_photo)
        f = open(CAPTCHA_IMAGE_FOLDER + '/' + chapter_photo.split('/')[-1], 'ab')
        f.write(img.content)
        f.close()
        m = m + 1
        time.sleep(3)
    page = page + 25

print('end')
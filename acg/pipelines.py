# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import requests
import os


class AcgPipeline(object):

    def process_item(self, item, spider):
        url = item['image_urls'][0]
        reference = item['image_referer'][0]
        Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                    'Connection': 'keep-alive',
                    'Referer': reference,
                    }
        image = requests.get(url, headers=Headers, timeout=6)
        form = item['image_form'][0]
        name = item['image_name'][0]
        drawer_name = item['drawer_name'][0]
        drawer_id = item['drawer_id'][0]
        floder_path1 = 'D://Project_pixiv/acg/test3/' + drawer_id + "/"
        floder_path2 = 'D://Project_pixiv/acg/test3/' + drawer_id + " " + drawer_name + "/"

        try:
            if not os.path.exists(floder_path2):
                os.makedirs(floder_path2)
            floder_path = floder_path2
        except OSError:
            if not os.path.exists(floder_path1):
                os.makedirs(floder_path1)
            floder_path = floder_path1
        finally:
            picture_path = floder_path + name + form
            f = open(picture_path, "wb")
            f.write(image.content)


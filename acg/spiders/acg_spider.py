# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 0008 22:32
# @Author  : allenx555
# @FileName: acg_spider.py
# @Software: PyCharm

import scrapy
from scrapy.http import Request
import requests
from scrapy import FormRequest
from acg.items import AcgItem
import urllib
import re
from lxml import etree


class acgSpider(scrapy.Spider):

    name = "acg"
    allowed_domains = ['pixiv.net', 'piximg.net']
    start_urls = "https://www.pixiv.net/bookmark.php?type=user"

    def start_requests(self):
        return [Request("https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
                        , callback=self.post_login)]

    def post_login(self, response):
        post_key = response.xpath('/html/body/div[3]/div[2]/form/input[1]/@value').extract()
        print("\n请输入账号：")
        pixiv_id = input()
        print("\n请输入密码：")
        password = input()
        return [FormRequest.from_response(response,
                                          formdata={
                                              'pixiv_id': pixiv_id,
                                              'password': password,
                                              'post_key': post_key,
                                          },
                                          callback=self.after_login,
                                          )]

    def after_login(self, response):
        yield self.make_requests_from_url(self.start_urls)

    def parse(self, response):
        try:
            nums = int(response.xpath('/html/body/div[4]/div[1]/div/div[2]/section/header/div/span/text()')
                       .extract()[0])
        except IndexError:
            print("输入账号或密码错误!")
            exit()
        pagenum = nums//48 + 2
        for i in range(1, pagenum):
            url = "https://www.pixiv.net/bookmark.php?type=user&rest=show&p=" + str(i)
            yield Request(url, callback=self.get_id)

    def get_id(self, response):
        ids = response.xpath("//a[@class='_user-icon size-75 cover-texture ui-profile-popup']/@data-user_id")\
            .extract()
        for id in ids:
            id_url = "https://www.pixiv.net/member_illust.php?id=" + str(id) + "&type=all&p=1"
            yield Request(id_url, callback=self.get_num)

    def get_num(self, response):
        id = response.url.replace("https://www.pixiv.net/member_illust.php?id=", "").replace("&type=all&p=1", "")
        pic_num = response.xpath("/html/body/div[4]/div[1]/div[1]/div/span/text()").extract()[0].replace("件", "")
        page_num = int(pic_num) // 20 + 2
        for j in range(1, page_num):
            url = "https://www.pixiv.net/member_illust.php?id=" + id + "&type=all&p=" + str(j)
            if j == 1:
                url = "https://www.pixiv.net/member_illust.php?id=" + id + "&type=all"
            yield Request(url, callback=self.get_pictureurl)

    def get_pictureurl(self, response):
        url = response.xpath("//a[@class='work  _work ']/@href").extract()
        reg1 = r'.+id=(\d+)&'
        drawer_id = re.findall(reg1, response.url)
        drawer_name = response.xpath("/html/head/title").extract()[0].replace("<title>「", "")\
            .replace("」 的作品 - 插画 [pixiv]</title>", "")
        error_id = []
        for pic_urls in url:
            pic_url = "https://www.pixiv.net" + pic_urls
            try:
                res1 = etree.HTML(requests.get(pic_url).text)
            except requests.exceptions:
                error_id.append(str(drawer_id))
                continue
            try:
                pic_xpath = res1.xpath("/html/body/div[6]/div/div[2]/div/div/div[1]/div[2]/a/img/@src")[0]
            except IndexError:
                error_id.append(str(drawer_id))
                continue
            picture_bash_url = pic_xpath.replace(
                "https://i.pximg.net/c/600x600/img-master/", "").replace("_master1200.jpg", "")
            fin_url = "https://i.pximg.net/img-original/" + picture_bash_url + ".jpg"
            reg = r'.+/(\d+)_p0'
            picture_id = re.findall(reg, fin_url)[0]

            Reference = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + picture_id
            Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                        'Connection': 'keep-alive',
                        'Referer': Reference
                       }

            try:
                req = urllib.request.Request(fin_url, None, Headers)
                res = urllib.request.urlopen(req, timeout=1)
                res.close()
                item = AcgItem()
                item['image_form'] = ['.jpg']
            except urllib.error.HTTPError:
                fin_url = fin_url.replace('.jpg', '.png')
                req = urllib.request.Request(fin_url, None, Headers)
                res = urllib.request.urlopen(req, timeout=1)
                res.close()
                item = AcgItem()
                item['image_form'] = ['.png']

            item['image_urls'] = [fin_url]
            item['image_referer'] = [Reference]
            item['image_name'] = [picture_id]
            item['drawer_id'] = drawer_id
            item["drawer_name"] = [drawer_name]

            yield item

        error_path = 'D://Project_pixiv/acg/test3/errorids.txt'
        f = open(error_path, "a")
        f.write('\n'.join(error_id))

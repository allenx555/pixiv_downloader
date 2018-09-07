# pixiv_downloader
a downloader for pixiv

## 说明
这是一个用于下载pixiv账户中所有关注画师的作品的scrapy爬虫

## 使用方法

### 注意事项
1. 使用前请自行加入pixiv的host
2.  爬虫使用了scrapy框架，请自行安装scrapy
3.  请自行添加 urllib，re，requests，lxml，os

### host的添加
host路径一般为 C:\Windows\System32\drivers\etc，用记事本打开并复制黏贴（host于2018.9.7更新）：

    #Pixiv
    210.129.120.52 www.pixiv.net
    210.140.131.144 source.pixiv.net
    210.129.120.42 accounts.pixiv.net
    210.140.131.144 imgaz.pixiv.net

## 使用
1. 在pychram中调试可通过entrypoint.py或main.py
2. 通过cmd运行请使用main.py
3. /acg/pipelines.py 内控制储存位置
4. 可能因为网络或各种原因存在个别图片下载失败，如果有下载失败则会在根目录下生成txt文件记录下载失败的图片的画师，请自行比对

### 其他
pixiv每日榜单下载链接：
[https://github.com/allenx555/pixiv_spider]()

'''
author : wbl2021
date:2021/04/29
'''
import requests
from lxml import etree
import time

dmbj_url = 'http://www.daomubiji.com/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}

def getTitles(main_page_url):
    '''
    获取小说每卷的名称和对于的地址
    :param main_page_url: 网站首页地址
    :return: （卷名，该卷地址）
    '''
    titles = []
    resp = requests.request("get", main_page_url, headers= header)
    selector = etree.HTML(resp.content.decode('utf-8'))   # 获取选择器
    li_tags = selector.xpath("//div[@class='sitenav']//li")  # 获取包含每卷名称和每卷地址的li标签
    for li in li_tags:
        title_name = li.xpath("./a/text()")[0]
        title_url = li.xpath("./a/@href")[0]
        titles.append([title_name, title_url])  # 注意：xpath返回的结果是列表
    titles = titles[1:]
    return titles

def getChapterList(title_url):
    '''
    获取该卷中所有章节的名称和对应的地址
    :param title_url: 该卷的地址
    :return: [[章节名称1，章节地址1], ...]
    '''
    # title_url = 'http://www.daomubiji.com/dao-mu-bi-ji-1'
    # chapters = []
    # resp = requests.request("get", title_url, headers = header)
    # html = resp.content.decode("utf-8")
    '''
    使用resp.content.decode()存在一个问题，如果面中有其他的字符编码，则在读取页面的时候会报UnicodeDecodeError: 'utf-8' codec can't decode byte 0xed这样的异常。
    使用resp.text返回的是Beautifulsoup根据猜测的编码方式将content内容编码成字符串，不需要额外进行编码，但是存在一个问题，.text不是所有时候显示都正常，这时就需要用.content进行手动编码
    由于此处异常内容不在爬虫范围内，故采用.text的方法规避异常
    '''
    resp = requests.get(title_url, headers = header)
    html = resp.text
    # print(html)
    selector = etree.HTML(html)
    aritcle_tags = selector.xpath("//div[@class='excerpts']//article")
    # print(aritcle_tags)
    for tag in aritcle_tags:
        yield [tag.xpath("./a/text()")[0], tag.xpath("./a/@href")[0]]  # 如果返回列表内容，由于列表内容较多，会占用较大的内存，此处使用生成器存放，使用时通过迭代获取
    # return chapters

def writeToFile(line):
    '''
    文本内容写入文件
    :param line: 文本内容
    :return: null
    '''
    with open('F:\dmbj\dmbj1.txt', 'a+') as f:
        f.write(line)


def getContent(chapter_name, chapter_url):
    '''
    获取每个章节的文本内容
    :param chapter_name: 章节名称
    :param chapter_url: 章节地址
    :return: Null
    '''
    writeToFile(chapter_name+"\n")
    # resp = requests.request("get", url = chapter_url, headers = header)
    # html = resp.content.decode("utf-8")
    resp = requests.get(url = chapter_url, headers = header)
    html = resp.text
    selector = etree.HTML(html)
    content_tags = selector.xpath("//article[@class='article-content']/p")
    for tag in content_tags:
        try:
            writeToFile(tag.xpath("./text()")[0]+"\n")
        except IndexError as e:
            print("抛出了一个%s异常，此处为文中的一处提示，格式与代码要求不符，需单独处理。" % e)
            if len(tag.xpath("./em/text()")) != 0:
                writeToFile(tag.xpath("./em/text()")[0]+"\n")


if __name__ == '__main__':
    start = time.time()
    titles = getTitles(dmbj_url)
    print("开始写入文章....")
    for title in titles:  # 遍历小说的卷名
        print("正在写入《"+title[0]+"》...")
        writeToFile(title[0]+"\n")  # 将卷名写入
        for chapter in getChapterList(title[1]):  # 遍历该卷中所有章节名称
            print("正在写入《"+chapter[0]+"》...")
            # print(chapter)
            getContent(chapter[0], chapter[1])  # 写入章节名称和章节内容
            print(chapter[0]+"写入完成.")
        print(title[0]+"写入完成.")
    end = time.time()
    h = time.strftime("%H:%M:%S", time.gmtime(end-start))
    print("全部写入完成，共耗时"+h)  # 总共耗时约16分钟
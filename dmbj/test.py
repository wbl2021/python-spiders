import requests
from lxml import etree
from urllib import request as req
if __name__ == '__main__':
    url ='http://www.daomubiji.com/2015-34.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}
    # res = requests.get(url, headers = header )
    # print(res.text.decode("utf-8"))
    resp = requests.request("get", url, headers= header)
    html = resp.text
    print(html)
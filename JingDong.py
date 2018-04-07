#coding utf-8
#author: ztx
#date: 2018-4-7
import requests
import re
import sys,locale
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
	"Accept": "image/webp,image/apng,image/*,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate,br",
	"Accept-Language": "zh-CN,zh,en-US,en;q=0.5",
	"Connection": "keep-alive",
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def getImgSrc(productId,page):
	#获取评论的地址
	COMMENT_URL = 'https://sclub.jd.com/comment/productPageComments.action'
	#构造获取评论的数据
	commentDatas = {
		'callback':'fetchJSON_comment98vv32769',
		'productId':productId,
		'score':'0',
		'sortType':'5',
		'page':page,
		'pageSize':'10',
		'isShadowSku':'0',
		'fold':'1'
	}
	html = requests.get(COMMENT_URL,params = commentDatas,headers = headers,verify=False)
	print(html.text)

if __name__ == '__main__':
	getImgSrc('5089235','0')
	pass

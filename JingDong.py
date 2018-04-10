#coding utf-8
#author: ztx
#date: 2018-4-7
'''
程序功能：
用来抓取京东评论区的数据。
本程序根据输入手机型号名称来抓取对应型号的URL并存入->data/【型号名文件夹】/【型号名】.txt
程序用法：
1.只需要在收集列表@phoneNames中添加需要收集的型号名称即可
2.本程序自动创建文件夹并存入，斟酌好收集的手机型号名称，保证不再改变。
3.每一个对应型号名称的抓取都会覆盖之前存入的txt文件，已经抓取过的手机型号，尽量不要再次运行程序
'''
import requests
import re
import json
import sys,locale
from bs4 import BeautifulSoup
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
	"Accept": "image/webp,image/apng,image/*,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate,br",
	"Accept-Language": "zh-CN,zh,en-US,en;q=0.5",
	"Connection": "keep-alive",
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def getProductID(productName):
	#获取搜索商品的地址
	SEARCH_URL = 'https://search.jd.com/search'
	#构造获取商品的URL参数
	searchDatas = {
		'keyword':productName,
		'enc':'utf-8',
		'qrst':'1',
		'rt':'1',
		'stop':'1',
		'vt':'2',
		#'wq':productName,
		'psort':'3',
		'click':'0',
		#'psort':'4',
		'bs':'1'
	}
	html = requests.get(SEARCH_URL,params = searchDatas,headers = headers)
	html_soup=BeautifulSoup(html.text,"html.parser")
	#print(html_soup)
	goodsList = html_soup.find('div',attrs={'id':'J_goodsList'})
	#print(goodsList)
	uls = goodsList.find('ul',attrs={'class':'gl-warp clearfix'})
	#print(uls)
	lis = uls.find_all('li',attrs={'class':'gl-item'})
	results = []
	#print(lis)
	#此处获取了所有的搜索页中手机型号的店家（ProductID标识）的HTML页面
	#然后我们抓取ProductID--->根据ProductID来进行
	for li in lis[0:30]:
		#获取商品ID,基本上一页就够了,一页有30个ProductID（不同商家的型号）
		try:
			item = li['data-sku']
			results.append(item)
		except:
			continue
	print(productName+" 的详细页面有:")
	print(results)
	return(results)

def getImgSrc(productId,page):
	#获取评论的地址
	COMMENT_URL = 'https://sclub.jd.com/comment/productPageComments.action'
	#构造获取评论的URL参数
	commentDatas = {
		'callback':'fetchJSON_comment98vv3231',
		'productId':productId,
		'score':'0',
		'sortType':'5',#商家推荐排序,图片多
		'page':page,
		'pageSize':'10',
		'isShadowSku':'0',
		'fold':'1'
	}
	try:	
		html = requests.get(COMMENT_URL,params = commentDatas,headers = headers)
		#使用正则表达式过滤字符串，找出所有评论图片的URL
		imageUrls = re.findall('img30.360buyimg.com/n0/s128x96_jfs(.*?)","a',str(html.text))
		#print(imageUrls)
		#构造大图片的URL,因为此前的图片是缩略图，根据URL的观察有如下结论：
		#URL中含有：img30.360buyimg.com/n0/s128x96_jfs 为128X86的缩略图
		#URL中含有：img30.360buyimg.com/shaidan/s616x405_jfs 为616x405的大图
		#其余的URL不会改变，所以可以根据缩略图URL构造大图URL,只需要更换一个头就可以了
		imageHead = "http://img30.360buyimg.com/shaidan/s616x405_jfs"
		results = set('')
		for imageUrl in imageUrls:
			imageUrl = imageHead + imageUrl
			results.add(imageUrl)
		return results
	except:
		print("获取出错")
		results = set('')
		return results
def getAll(phoneName):
	productIds = getProductID(phoneName)
	allUrls = set()
	for productId in productIds:
		print("商品ID:"+productId)	
		#亲测只能获取100页评论，多了不行
		for page in range(0,100):
			try:
				imageUrls = getImgSrc(productId,page)
				if(imageUrls == set('')):
					continue
				#此处是去除重复操作，集合的 | ----> "或" "取交集" "去除重复"
				allUrls = allUrls|imageUrls
				print("第"+str(page)+"页的URL已获取")
			except:
				print("获取URL出错")
				continue
	saveToCSV(phoneName,allUrls)

def saveToCSV(phoneName,texts):
	#一次性将集合中元素(texts)写入txt
	path = "./data/"+phoneName+"/"
	mkdir(path)
	file_writer = open(path+phoneName+".txt",'w',encoding='utf-8')
	datas = ""
	i = 0
	for data in texts:
		i = i + 1
		datas = datas + str(i) + " " + data +"\n"
	if file_writer.write(datas):
		print(phoneName+"手机的全部数据写入成功")
	else:
		print(phoneName+"手机的全部数据写入失败")
	file_writer.close()
def mkdir(path):
	#创建件文件夹
	isExists=os.path.exists(path)
	# 判断结果
	if not isExists:
		os.makedirs(path) 
		print (path+' 创建成功')
		return True
	else:
		# 如果目录存在则不创建，并提示目录已存在
		print (path+' 目录已存在')
		return False
if __name__ == '__main__':
	#getImgSrc('5089235','1')
	#'三星s9','三星s8','华为p10','华为mate10','一加5','一加5T','坚果pro2','坚果pro','魅蓝E','iphone8plus','iphonex',
	#'乐视pro3','红米5a','小米mix2','小米6','华为荣耀9','华为畅玩7x','vivox20','oppor11s','华为畅享6'
	
	'''
	以上手机型号全部获取!！
	请谨慎更改phoneNames中的值
	一旦再次运行将覆盖原有的存储对应URL的txt文件！！
	'''
	phoneNames = []

	'''
	强烈建议一次只抓一种手机型号，也就是直接更改 phoneName 的值,这样方便出错检查！
	example：

	if __name__ == '__main__':
		getAll('三星s8')

	'''
	for phoneName in phoneNames:
		#获取手机名称的京东评论图片、并存储URL值到txt文件中
		getAll(phoneName)
	
	
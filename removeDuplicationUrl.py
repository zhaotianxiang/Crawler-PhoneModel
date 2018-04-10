#coding utf-8
#author: ztx
#date: 2018-4-7
#程序的目的是去除重复的URL。
#实现很简单，先读入set，再从set中读取后写入uniqueUrls.txt
import os

def readFromTxt(phoneName):
	retsults = set()
	path = "./data/"+phoneName+"/"
	file_reader = open(path+phoneName+".txt",'r',encoding='utf-8')
	for line in file_reader.readlines():
		item = line.split(" ")
		url = item[1]
		retsults.add(url)
	file_reader.close()
	return retsults

def saveToTxt(phoneName,sets):
	path = "./data/"+phoneName+"/"
	file_writer = open(path+"uniqueUrls.txt",'w',encoding='utf-8')
	datas = ""
	i = 0
	for data in sets:
		i = i + 1
		datas = datas + str(i) + " " + data
	if file_writer.write(datas):
		print(phoneName+"手机的全部数据写入成功")
	else:
		print(phoneName+"手机的全部数据写入失败")
	file_writer.close()

if __name__ == '__main__':
	#getImgSrc('5089235','1')
	#'三星s9','三星s8','华为p10','华为mate10','一加5','一加5T','坚果pro2','坚果pro','魅蓝E','iphone8plus','iphonex',
	#'乐视pro3','红米5a','小米mix2','小米6','华为荣耀9','华为畅玩7x','vivox20','oppor11s','华为畅享6'
	phoneNames = ['三星s9','三星s8','华为p10','华为mate10','一加5','一加5T','坚果pro2',
	'坚果pro','魅蓝E','iphone8plus','iphonex','乐视pro3','红米5a','小米mix2','小米6',
	'华为荣耀9','华为畅玩7x','vivox20','oppor11s','华为畅享6']
	for phoneName in phoneNames:
	#去除重复后的Urls
		uniqueUrls = readFromTxt(phoneName)
		saveToTxt(phoneName,uniqueUrls)
	#########################################
	# 后来发现想多了，根本没有重复
	# #######################################
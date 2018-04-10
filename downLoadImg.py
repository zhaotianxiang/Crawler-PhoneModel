#coding utf-8
#author: ztx
#date: 2018-4-7
#程序的目的是去根据文件中的url来下载图片。
#考虑使用多线程或者多进程
'''
程序用法：
1.必须先用抓URL的程序抓取对应型号的URL存入->data/【型号名文件夹】/uniqueUrls.txt
2.本程序自动读取uniqueUrls.txt文件中的URL进行图片的下载
3.两个程序没有合并在一起（为了文件检查），注意手机型号名称一定要对应一致
'''
import os
import urllib.request

def downLoadImgByPhoneName(phoneName):
	path = "./data/"+phoneName+"/"
	file_reader = open(path+"uniqueUrls.txt",'r',encoding='utf-8')
	for line in file_reader.readlines():
		item = line.split(' ')
		index = item[0]
		url = item[1].replace('\n','')
		if os.access(path+index+".jpg", os.F_OK):
			continue
		try:
			urllib.request.urlretrieve(url,path+index+".jpg")
			print(url+"成功获取")
		except:
			print("地址："+url+"图片下载失败")
			continue
	file_reader.close()

if __name__ == '__main__':
	#'三星s9','三星s8','华为p10','华为mate10','一加5','一加5T','坚果pro2','坚果pro','魅蓝E','iphone8plus','iphonex',
	#'乐视pro3','红米5a','小米mix2','小米6','华为荣耀9','华为畅玩7x','vivox20','oppor11s','华为畅享6'
	phoneNames = ['三星s9','三星s8','华为p10','华为mate10','一加5','一加5T','坚果pro2',
	'坚果pro','魅蓝E','iphone8plus','iphonex','乐视pro3','红米5a','小米mix2','小米6',
	'华为荣耀9','华为畅玩7x','vivox20','oppor11s','华为畅享6']
	for phoneName in phoneNames:
		downLoadImgByPhoneName(phoneName)
	print("下载全部完成")


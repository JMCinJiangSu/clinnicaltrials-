# 临床试验筛选流程
# ! /usr/bin/python3
# -*- coding = utf-8 -*-

'''
嵇梦晨
2021-12-08

'''

import re
import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import shutil
import openpyxl
import datetime


def datafile(path):
	# 0.原始xml文件处理，提取recruiting的条目
	# path = '/mnt/e/Update/clinicaltrials/AllPublicXML'
	# 每个月更新一次，从clinical trials网站下载最新的压缩包
	for root, dirs, files in os.walk(path):
		for f in files:
			if '.xml' in f:
				tree = ET.parse(f)
				root2 = tree.getroot()
				status = root2.find('overall_status')
				if status.text == 'Recruiting':
					try:
						shutil.copy(path + '/' + str(f), path + '/' + 'Recruiting')
						print(f)
					except shutil.SameFileError:
						pass
	for root, dirs, files in os.walk(path + '/' + 'Recruiting'):
		filename = []
		for f in files:
			nct_id = str(f[:-4])
			filename.append(nct_id)
	return(filename)

def main():
	df = pd.read_excel('/mnt/e/Update/clinicaltrials/临床试验最终版.xlsx')
	nct = []
	for i in df.index:
		nct.append(df.loc[i, 'NCT Number'])
	
	path = '/mnt/e/Update/clinicaltrials/AllPublicXML'
	recruiting_NCT = datafile(path)

	NotRecruiting = [val for val in nct if val not in recruiting_NCT]

	DelIndex = []
	for j in df.index:
		for val in NotRecruiting:
			if df.loc[j, 'NCT Number'] == val:
				DelIndex.append(j)
	df.drop(index = DelIndex, inplace = True)

	writer = pd.ExcelWriter('临床试验new.xlsx', engine = 'openpyxl')
	df.to_excel(writer, index = False)
	writer.save()



if __name__ == '__main__':
	starttime = datetime.datetime.now()
	main()
	end = datetime.datetime.now()
	print(end-starttime)








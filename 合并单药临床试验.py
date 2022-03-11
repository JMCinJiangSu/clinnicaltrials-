# 合并单药临床试验
# ! /usr/bin/python3
# -*- coding = utf-8 -*-

'''
嵇梦晨
2021-12-09

'''
import re
import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import shutil
import openpyxl
import datetime

filename = os.listdir('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验')

col = ['靶向药物', 'NCT Number', '临床试验内容', 'Phases', '地点', '癌种', '靶点', 'criteria']
dfall = pd.DataFrame(columns = col)

for i in filename:
	df = pd.read_excel('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/' + i)
	dfall = pd.concat([dfall, df], axis = 0)

writer = pd.ExcelWriter('单药合并结果.xlsx', engine = 'openpyxl')
dfall.to_excel(writer, index = False)
writer.save()

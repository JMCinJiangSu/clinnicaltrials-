# ! /usr/bin/python3
# -*- coding = utf-8 -*-

import re
import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import shutil
import openpyxl
import datetime

def OldNCT():
    df = pd.read_excel('/mnt/e/Update/clinicaltrials/临床试验最终版.xlsx')
    nct = []
    for i in df.index:
        nct.append(df.loc[i, 'NCT Number'])
    return(nct)
old = OldNCT()
print('老版NCT获取完成')
df2 = pd.read_excel('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/单药合并结果.xlsx')
nct = []
for f in df2.index:
    nct_id = df2.loc[f, 'NCT Number']
    nct.append(nct_id)

nct2 = []
for item in nct:
    if not item in nct2:
        nct2.append(item)
print('新版NCT获取完成')
add = [val for val in nct2 if not val in old]


col = ['靶向药物', 'NCT Number', '临床试验内容', 'Phases', '地点', '癌种', '靶点', 'criteria']
df = pd.DataFrame(columns = col)

for i in add:
    for j in df2.index:
        if df2.loc[j, 'NCT Number'] == i:
            df = df.append(df2.loc[j], ignore_index = True)
            print(i)

writer = pd.ExcelWriter('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/新增临床试验.xlsx', engine = 'openpyxl')
df.to_excel(writer, index = False)
writer.save()

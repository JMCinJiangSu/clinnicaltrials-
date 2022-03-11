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

def datafile(path):
    # 0.原始xml文件处理，提取recruiting的条目
	# path = '/mnt/e/Update/clinicaltrials/AllPublicXML'
	# 每个月更新一次，从clinical trials网站下载最新的压缩包
    if not os.path.exists(path + '/' + 'Recruiting'):
        os.makedirs(path + '/' + 'Recruiting')

    for root, dirs, files in os.walk(path):
        for f in files:
            name = os.path.join(root, f)
            if 'xml' in str(name):
                tree = ET.parse(str(name))
                root2 = tree.getroot()
                status = root2.find('overall_status')
                if status.text == 'Recruiting':
                    shutil.copy(str(name), path + '/' + 'Recruiting')
                    print(f)

def intervention(root):
	# 1.对intervention进行筛选，以靶药为关键词
	intervention = root.findall('intervention')
	# 获取所有intervention
	intervention_name = []
	for name in intervention:
		a = name.find('intervention_name').text
		intervention_name.append(a)
	return(intervention_name)

def condition(root):
	condition = root.findall('condition')
	# 2.对condition进行筛选，肿瘤相关
	conditions = []
	for disease in condition:
		conditions.append(disease.text)
	return('|'.join(conditions))

def country(root):
	# 3.提取进行临床试验的地点，国家
	location = root.find('location_countries')
	countries = []
	for country in location:
		countries.append(country.text)
	return('|'.join(countries))

def criteria(root):
	# 4.加入入组标准
	criteria = root.find('eligibility')
	Inclusion_criteria = ''
	for inclusion in criteria:
		try:
			inclusion.find('textblock').text
			Inclusion_criteria += inclusion.find('textblock').text
		except :
			pass
	return(Inclusion_criteria)

def Summary(root):
    # 提取摘要
    summary = root.find('brief_summary')
    txt = ''
    for val in summary:
        try:
            summary.find('textblock').text
            txt += summary.find('textblock').text
        except:
            pass
    return(txt)

def target(Inclusion_criteria):
	# 5.提取入组标准中关键词，药物靶点
	Genes = ['AKT1', 'AKT2', 'ALK', 'ARID1A', 'ATM', 'ATR', 'ATRX', 'BRAF', 'BRCA1', 'BRCA2',
	'BRIP1', 'CCND1', 'CCND2', 'CDK12', 'CDK4', 'CDK6', 'CDKN2A', 'CHEK1', 'CHEK2', 'CSF1R',
	'CTNNB1', 'dMMR', 'EGFR', 'ERBB2', 'HER2', 'ERBB3', 'FGFR1', 'FGFR2', 'FGFR3', 'IDH1', 'KDR',
	'KIT', 'KRAS', 'MED12', 'MET', 'MSI-H', 'NF1', 'NF2', 'NRAS', 'NTRK', 'PALB2', 'PDGFRA',
	'PIK3CA', 'PTEN', 'RAC1', 'RAD50', 'RAD51C', 'RAD51D', 'RAF1', 'RAS', 'RB1', 'RET', 'ROS1',
	'SDHB', 'SDHC', 'SDHD', 'STK11', 'TMB-H', 'TP53', 'TSC1', 'TSC2', 'VEGFR', 'VHL', 'RAD51C/D', 'CDK4/6',
    'BRCA1/2', 'FGFR', 'RET']
	target_genes = []
	for gene in Genes:
		if gene in Inclusion_criteria:
			target_genes.append(gene)
	return('|'.join(target_genes))

def target2(summary):
    Genes = ['AKT1', 'AKT2', 'ALK', 'ARID1A', 'ATM', 'ATR', 'ATRX', 'BRAF', 'BRCA1', 'BRCA2',
    'BRIP1', 'CCND1', 'CCND2', 'CDK12', 'CDK4', 'CDK6', 'CDKN2A', 'CHEK1', 'CHEK2', 'CSF1R',
    'CTNNB1', 'dMMR', 'EGFR', 'ERBB2', 'HER2', 'ERBB3', 'FGFR1', 'FGFR2', 'FGFR3', 'IDH1', 'KDR',
    'KIT', 'KRAS', 'MED12', 'MET', 'MSI-H', 'NF1', 'NF2', 'NRAS', 'NTRK', 'PALB2', 'PDGFRA',
    'PIK3CA', 'PTEN', 'RAC1', 'RAD50', 'RAD51C', 'RAD51D', 'RAF1', 'RAS', 'RB1', 'RET', 'ROS1',
    'SDHB', 'SDHC', 'SDHD', 'STK11', 'TMB-H', 'TP53', 'TSC1', 'TSC2', 'VEGFR', 'VHL', 'RAD51C/D', 'CDK4/6',
    'BRCA1/2', 'FGFR', 'RET']
    target_genes = []
    for gene in Genes:
        if gene in summary:
            target_genes.append(gene)
    return('|'.join(target_genes))

def info(root):
	# 6.加入nct_id,title, phase
	nct = root.find('id_info').find('nct_id').text
	title = root.find('brief_title').text
	phase = root.findall('phase')
	phases = []
	for i in phase:
		phases.append(i.text)
	trialsinfo = [nct, title, '|'.join(phases)]
	return(trialsinfo)

def OldNCT():
    # 7.获取上一版本数据库中NCT编号
    df = pd.read_excel('/mnt/e/Update/clinicaltrials/临床试验最终版.xlsx')
    nct = []
    for i in df.index:
        nct.append(df.loc[i, 'NCT Number'])
    return(nct)

def DelNotRecruit(oldnct, recruiting_NCT):
    # 8. 删除不再招募的临床试验，生成新的excel文件
    # oldnct：OldNCT函数返回的列表
    # recruiting_NCT: Recruiting文件夹中的文件名
    NotRecruiting = [val for val in oldnct if val not in recruiting_NCT]
    f = open('不再招募NCT编号.txt', 'w+')
    f.write('\n'.join(NotRecruiting))
    f.close()

    df = pd.read_excel('/mnt/e/Update/clinicaltrials/临床试验最终版.xlsx')
    DelIndex = []
    for i in df.index:
        for val in NotRecruiting:
            if df.loc[i, 'NCT Number'] == val:
                DelIndex.append(i)
    df.drop(index = DelIndex, inplace = True)
    writer = pd.ExcelWriter('/mnt/e/Update/clinicaltrials/AllPublicXML/临床试验-去除未招募.xlsx', engine = 'openpyxl')
    df.to_excel(writer, index = False)
    writer.save()

def MergeDrug():
    col = ['靶向药物', 'NCT Number', '临床试验内容', 'Phases', '地点', '癌种', '靶点', 'criteria', 'brief_summary']
    filename_new = os.listdir('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验')
    dfall = pd.DataFrame(columns = col)
    for i in filename_new:
        df = pd.read_excel('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/' + i)
        dfall = pd.concat([dfall, df], axis = 0)
    writer = pd.ExcelWriter('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/单药合并结果.xlsx', engine = 'openpyxl')
    dfall.to_excel(writer, index = False)
    writer.save()

def main():
    path = '/mnt/e/Update/clinicaltrials/AllPublicXML'
    try:
        datafile(path)
    except:
        pass
    # 读取XML文件名
    filename = os.listdir('/mnt/e/Update/clinicaltrials/AllPublicXML/Recruiting')
    nct = []
    for f in filename:
        nct_id = f[:-4]
        nct.append(nct_id)
    old = OldNCT()
    DelNotRecruit(old, nct) # 去除上版本数据库中不再招募的临床试验
    
    # 读取靶药列表
    drug = []
    with open('/mnt/e/Update/clinicaltrials/靶药列表.txt') as f:
        for line in f:
            line = line.strip()
            drug.append(line)
    # 设置生成excel文件列名
    col = ['靶向药物', 'NCT Number', '临床试验内容', 'Phases', '地点', '癌种', '靶点', 'criteria', '靶点2','brief_summary']
    
    if not os.path.exists('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验'):
        os.makedirs('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验')

    for val in drug:
        print(val)
        df = pd.DataFrame(columns=col)
        j = 0
        for i in filename:
            tree = ET.parse('/mnt/e/Update/clinicaltrials/AllPublicXML/Recruiting' + '/' + i)
            root = tree.getroot()
            intervention_name = intervention(root)
            intervention_name = ''.join(intervention_name).lower()

            if val in intervention_name:
                diseases = condition(root)
                countries = country(root)
                criteries = criteria(root)
                summary = Summary(root)
                target_genes = target(criteries)
                target_genes2 = target2(summary)
                otherinfo = info(root)
                df.loc[j, '靶向药物'] = val
                df.loc[j, 'NCT Number'] = otherinfo[0]
                df.loc[j, '临床试验内容'] = otherinfo[1]
                df.loc[j, 'Phases'] = otherinfo[2]
                df.loc[j, '地点'] = countries
                df.loc[j, '癌种'] = diseases
                df.loc[j, '靶点'] = target_genes
                df.loc[j, 'criteria'] = criteries
                df.loc[j, '靶点2'] = target_genes2
                df.loc[j, 'brief_summary'] = summary
                print(i)
            j += 1
        writer = pd.ExcelWriter('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/' + val + '.xlsx', engine='openpyxl')
        df.to_excel(writer, val, index = False)
        writer.save()
    
    MergeDrug()

    add = [val for val in nct if not val in old]
    df1 = pd.DataFrame(columns=col)
    df2 = pd.read_excel('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/单药合并结果.xlsx')
    for item in add:
        for k in df2.index:
            if df2.loc[k, 'NCT Number'] == item:
                df1 = df1.append(df2.loc[k], ignore_index=True)
    writer = pd.ExcelWriter('/mnt/e/Update/clinicaltrials/AllPublicXML/单药临床试验/新增临床试验.xlsx', engine = 'openpyxl')
    df1.to_excel(writer, index=False)
    writer.save()

if __name__ == '__main__':
	starttime = datetime.datetime.now()
	main()
	end = datetime.datetime.now()
	print(end-starttime)

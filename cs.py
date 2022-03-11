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

def main():
	
	new = []
	with open('重筛靶点.txt') as f:
		for line in f:
			line = line.strip()
			new.append(line)

	col = ['靶向药物', 'NCT Number', '临床试验内容', 'Phases', '地点', '癌种', '靶点', 'criteria', '靶点2','brief_summary']

	df = pd.DataFrame(columns = col)
	j = 0
	for i in new:
		tree = ET.parse('/mnt/e/Update/clinicaltrials/AllPublicXML/Recruiting' + '/' + i + '.xml')
		root = tree.getroot()
		intervention_name = intervention(root)
		intervention_name = ''.join(intervention_name).lower()
		diseases = condition(root)
		countries = country(root)
		criteries = criteria(root)
		summary = Summary(root)
		target_genes = target(criteries)
		target_genes2 = target2(summary)
		otherinfo = info(root)
		
		df.loc[j, 'NCT Number'] = otherinfo[0]
		df.loc[j, '临床试验内容'] = otherinfo[1]
		df.loc[j, 'Phases'] = otherinfo[2]
		df.loc[j, '地点'] = countries
		df.loc[j, '癌种'] = diseases
		df.loc[j, '靶点'] = target_genes
		df.loc[j, '靶点2'] = target_genes2
		df.loc[j, 'criteria'] = criteries
		df.loc[j, 'brief_summary'] = summary
		j += 1
	writer = pd.ExcelWriter('/mnt/e/Update/clinicaltrials/AllPublicXML/重筛结果.xlsx', engine='openpyxl')
	df.to_excel(writer, index = False)
	writer.save()


if __name__ == '__main__':
	starttime = datetime.datetime.now()
	main()
	end = datetime.datetime.now()
	print(end-starttime)
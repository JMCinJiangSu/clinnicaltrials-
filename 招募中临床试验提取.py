# ! /usr/bin/python3
# -*- coding = utf-8 -*-
import re
import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import shutil

path = '/mnt/e/Update/clinicaltrials/AllPublicXML'
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
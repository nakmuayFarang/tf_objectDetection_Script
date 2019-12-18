#!/usr/bin/env python
# coding: utf-8

'''
Loop throught pathX/sample and read xml
create a csv file in pathAnnotation
'''


import argparse
import os
import xml.etree.ElementTree as ET
import pandas as pd
from math import floor
import sys

sample = sys.argv[1]

pathScript = str(os.path.dirname(os.path.abspath(__file__))) + '/'

param = '../' + 'param.json'

if not os.path.isfile(param):
	with open(param,'w') as jsn:
		jsn.write('{"pathData" : ""\n,"pathX" :"" \n,"pathAnnotation" : ""\n}')
		assert False, "Fill param.json"

with open(param) as jsn:
	jsn = json.load(jsn)

pathX = jsn['pathX'] "{}/".format(sample)
pathAnnotation = jsn["pathAnnotation"]

assert os.path.exists(pathX),' "pathX/{}/": "{}" is not a valid path'.format(sample,pathX)
assert os.path.exists(pathAnnotation),' "pathAnnotation": "{}" is not a valid path'.format(pathAnnotation)

ret = dict()
ret['filename'] = []
ret['width'] = []
ret['height'] = []
ret['class'] = []
ret['xmin'] = []
ret['ymin'] = []
ret['xmax'] = []
ret['ymax'] = []


with open(pathAnnotation + sample + '.txt') as f:
	files = f.readlines()

n = len(files)
cpt = 1

for file in files:
	#Loop through Y folder
	if round(cpt * 100 /n,0) % 10 < round((cpt - 1) * 100 /n,0)%10:
		print("{}% done".format(round(cpt * 100 /n,0)))
	
	XML = ET.parse(pathX + file[:-1] + '.xml').getroot()
	filename = XML.find('filename').text
	width = int(XML.find('size').find('width').text)
	height = int(XML.find('size').find('height').text)
	for obj in XML.findall('object'):
		#Loop throught detected faces
		ret['class'].append(obj.find('name').text)
		ret['xmin'].append(int(obj.find('bndbox').find('xmin').text))
		ret['xmax'].append(int(obj.find('bndbox').find('xmax').text))
		ret['ymin'].append(int(obj.find('bndbox').find('ymin').text))
		ret['ymax'].append(int(obj.find('bndbox').find('ymax').text))
		ret['filename'].append(filename)
		ret['width'].append(width)
		ret['height'].append(height)
	cpt += 1


ret = pd.DataFrame.from_dict(ret)

ret.to_csv(pathAnnotation + '{}.csv'.format(sample))
print(sample + ".csv created" )

"""Create training and test sample
80% de train, 20% de test.
This script create 2 text files contening the name of the file
"""


import os
import random
import sys
import json


pathScript = str(os.path.dirname(os.path.abspath(__file__))) + '/'


os.chdir(pathScript)

param = '../' + 'param.json'

if not os.path.isfile(param):
	with open(param,'w') as jsn:
		jsn.write('{"pathData" : ""\n,"pathX" :"" \n,"pathAnnotation" : ""\n}')
		assert False, "Fill param.json"


with open(param) as jsn:
	jsn = json.load(jsn)


pathData =  jsn["pathData"]
pathAnnotation = jsn['pathAnnotation'] + '{}'

assert os.path.exists(pathData),' "pathData": "{}" is not a valid path'.format(pathData)
assert os.path.exists(pathAnnotation), ' "pathAnnotation": "{}" is not a valid path'.format(pathAnnotation)

files = os.listdir(pathData)
files = list( map(lambda s: s.split('.')[0],files ) )#no file extension
random.shuffle(files)
ntrain = int( round(80 * len(files)/100,0))


train = files[0:ntrain]
test = files[ntrain:]

with open( pathAnnotation.format("train.txt"),'w') as t:
	for x in train:
		t.write(x + '\n')
print("train.txt created")

with open(pathAnnotation.format("test.txt"),'w') as t:
	for x in test:
		t.write(x + '\n')
print("test.txt created")


"""
Create workspace directory and all the subdirectory
	-If tensorflow folder already contain a workspace forlder, rename it workspace_i
	-Create a neaw workspace directory

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
		jsn.write('{ "pathTf_ObjDetection_Api" : ""\n, "pathData" : ""\n,"pathX" :"" \n,"pathAnnotation" : ""\n}')
		assert False, "Fill param.json"


with open(param) as jsn:
	jsn = json.load(jsn)

pathTf = jsn["pathTf_ObjDetection_Api"]

assert os.path.exists( pathTf + 'models'), 'Error in param.json; "pathTf_ObjDetection_Api":"{}" is not a valid path!'.format(pathTf)



os.chdir(pathTf)


if os.path.exists("workspace"):
	i = 0
	while os.path.exists("workspace_{}".format(i)):
		i+=1
	os.rename("workspace/","workspace_{}".format(i))

os.mkdir("workspace/")

os.mkdir("workspace/training_demo/")
os.chdir("workspace/training_demo/")

copyfile(pathTf + '/models/research/object_detection/legacy/train.py',os.getcwd() + '/train.py')
copyfile(path_tf + '/models/research/object_detection/export_inference_graph.py', os.getcwd() + '/export_inference_graph.py')

for dir in ["annotations","images/","images/test/","images/train/","pre-trained-model/","training/"]:
	os.mkdir(dir)



print("Done")
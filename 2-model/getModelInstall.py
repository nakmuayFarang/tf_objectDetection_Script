



import os
import urllib.request
from bs4 import BeautifulSoup
import json
import platform
import sys

assert platform.system()!='Darwin', 'Change your os! Linux: https://ubuntu.com/download/desktop'

if platform.system()=='Windows':
	print('U should considering changeing your os to Linux: https://ubuntu.com/download/desktop ')
	ext = 'bat'
elif platform.system()=='Linux':
	ext='sh'

pathScript = str(os.path.dirname(os.path.abspath(__file__))) + '/'
pathLauncher = pathScript + 'launcher/'

def CreateBat():
	urlZoo = "https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md"
	pathLauncher = pathScript + 'laucher/'

	os.mkdir(pathLauncher )

	html = urllib.request.urlopen( urlZoo)
	soup = BeautifulSoup(html,features="lxml")


	tables = soup.find_all('table')
	for table in tables:
		rows = table.find('tbody').find_all('tr')
		for row in rows:
			collect = row.find('td').find('a',href=True)
			with open(pathLauncher + 'get_{}.{}'.format(collect.text,ext),'w') as modelFile:
				modelFile.write( 'python {}getModelInstall.py {}'.format(pathScript,collect['href'].split('/')[-1].split('.')[0]  ).replace('/','\\') )


def LoadModel(mdl):
	from shutil import copyfile
	import sys
	import os
	import urllib.request as request
	import tarfile
	modelName = sys.argv[1]
	urlTfModelZoo = 'http://download.tensorflow.org/models/object_detection/{}.tar.gz'
	pathModel = path_tf + 'workspace/training_demo/pre-trained-model/'
	modelScipt = path_tf + 'workspace/training_demo/training/' + modelName + '/'
	#Create model script file
	os.mkdir( modelScipt + '/')
	if not os.path.isdir(pathModel + modelName):
		#add not between if and os.path
		os.chdir(pathModel)
		print('Download the model')
		pathModel += modelName + '.tar.gz'
		request.urlretrieve(urlTfModelZoo.format(modelName),pathModel)
		print('Extract the model')
		file = tarfile.open(pathModel)
		file.extractall()
		file.close()
		os.remove(pathModel)
		print("copy config file from pre-trained-model to trained-modelining")
		copyfile(pathModel[:-7] + "/pipeline.config",modelScipt + "pipeline.config")
		print("create training model bat")
		with open(path_tf + 'workspace/training_demo/train_{}.bat'.format(modelName),'w' ) as bat:
			bat.write("python train.py --logtostderr --train_dir=training/{}/ --pipeline_config_path=training/{}/pipeline.config".format(modelName,modelName))
		with open(path_tf + 'workspace/training_demo/exportInference_{}.bat'.format(modelName),'w' ) as bat:
			bat.write("python export_inference_graph.py --input_type image_tensor --pipeline_config_path training/{}/pipeline.config --trained_checkpoint_prefix training/{}/model.ckpt-Step --output_directory training/{}/trained-inference-graphs-Step/output_inference_graph_v1.pb".format(modelName,modelName,modelName))

		print('Successfuly done')

pathScript = str(os.path.dirname(os.path.abspath(__file__))) + '/'
os.chdir(pathScript)
param = '../' + 'param.json'

if not os.path.isfile(param):
	with open(param,'w') as jsn:
		jsn.write('{"pathData" : ""\n,"pathX" :"" \n,"pathAnnotation" : ""\n}')
		assert False, "Fill param.json"

with open(param) as jsn:
	jsn = json.load(jsn)

path_tf = jsn['pathTf_ObjDetection_Api'] 


assert os.path.exists(path_tf),' "pathTf_ObjDetection_Api": "{}" is not a valid path'.format(path_tf)


if len(sys.argv)==1:
	CreateBat()
else:
	mdl = sys.argv[1]
	LoadModel(mdl)

# Tensorflow object detection API

Setup workspace env for tensorflow object detection API.<br>
https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html

This repo has to be clone in Tensoflow folder (Same directory model) :<br>
Open a terminal and run:

```
>cd [Path Tensorflow]\
>git clone ssh:github.com/nakmuayFarang/tf_objectDetection_Script.git
```

## I Preprocessing

### Fill param.json

This json contain the paths of the project:
- pathTf_ObjDetection_Api: tensorflow path (this folder contains models [tensorflow object detection API])
- pathData: Path of the pictures (Original pictures)
- pathX: Path of the pictures inputs and xml output of the detection models
- pathAnnotation: This directory contain labels (.pbtxt file), csv, .record files

```
>cd scripts
>Notepad param.json
>::Fill this file with the differents paths; save then close
```


### 0-createWorkspace
Create all the dirs and subdir of workspace.


```
>cd 0-createWorkspace\
>python createWorkspace.py
>cd ../
```



### 1-preprocessing

This script has to be run using the object detection env (for me tf_1.4).


```
>cd 1-preprocessing\
>activate tf_1.4
>runPreprocessing
>../
```

### 2-model

Create bat file downloading and extracting the model from tensorflow model zoo


#### Create Launcher

getModelInstall.py must be run from Scrapping envs (requiere bs4).
Create for each model of tensorflow model zoo a bat file downloading and setting up everything for the training.

### Load a model
For loading a model just run the bat file corresponding to the model
- The bat file will download and extract the model in pretrained_model/modelname/
- Copy the pipeline.config file from pretrained_model/modelname/ to training/modelname/pipeline.config
- Create in training_demo a bat file that run for this model the training
- Create export_inference bat file, that create a model in training/modelname/trained-inference-graphs-Step/

User have to fill the pipeline.config file from training/model/pipeline.config.

```
>activate Scrapping
>cd 2-model\
>python getModelInstall.py
>cd launcher/
>get_modelName.bat
>conda deactivate
>cd ../../../workspace\training_demo\training\modelName\
>Notepad pipeline.config
>:: Fill it; save and close the files
>cd ../../
```



## II Train the model


### Run the training
From training_demo run train_modelname.bat using object detection env.

```
>train_modelName.bat
```
press Ctrl + C for stopping the training.


### Monitor the training

Open a new terminal and, using tf_1.4 env open a tensorboard.

```
>cd [Tensorflow Path]\workspace\training_demo\
>activate tf_1.4
>tensorboard --logdir=training/modelName/
```

Open a new terminal and write:
```
>cd "C:\Program Files\Mozilla Firefox"
>firefox http://%computername%:6006/
```

## III Export the model

From training_dem folder, tf_1.4 envs:
- Open exportInference_modelName.bat and replace 'Step' by the last training iteration
- Save and run this exportInference_modelName.bat

``` 
activate tf_1.4
>cd [Tensoflow Path]\workspace\training_demo
>Notepad exportInference_modelName.bat
>:: Fill with the desired step; save and close
>exportInference_modelName.bat
```


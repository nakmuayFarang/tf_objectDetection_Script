

::Run from tf_1.4 envs
python 1-createTestTrain.py
python 2-createCSV.py test
python 2-createCSV.py train
python 3-generate_tfrecord.py test
python 3-generate_tfrecord.py train


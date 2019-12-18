

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf
import sys
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

sample = sys.argv[1]

pathScript = str(os.path.dirname(os.path.abspath(__file__))) + '/'

param = '../' + 'param.json'

if not os.path.isfile(param):
	with open(param,'w') as jsn:
		jsn.write('{"pathData" : ""\n,"pathX" :"" \n,"pathAnnotation" : ""\n}')
		assert False, "Fill param.json"

with open(param) as json:
	json = json.load(json)

pathImg = json['pathX'] "{}/".format(sample)
pathOutput = json["pathAnnotation"]

assert os.path.exists(pathImg),' "pathX/{}/": "{}" is not a valid path'.format(sample,pathImg)
assert os.path.exists(pathOutput),' "pathAnnotation": "{}" is not a valid path'.format(pathOutput)


def class_text_to_int(row_label):
    if row_label == "face":
        return 1
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group):
    with tf.gfile.GFile(pathImg + '{}.jpg'.format(group.filename), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    # check if the image format is matching with your images.
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(pathOutput + '{}.record'.format(sample))
    examples = pd.read_csv(pathOutput + "{}.csv".format(sample))
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = pathOutput + '{}.record'.format(sample)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
import numpy as np
import os

import pymongo
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
import pylab
from matplotlib import pyplot as plt
from PIL import Image
import object_detection.utils.label_map_util as label_map_util
import object_detection.utils.visualization_utils as vis_util


# if tf.__version__ < '1.4.0':
#     raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

class ObjectDetector:
    # What model to download.
    # MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
    # MODEL_NAME = 'faster_rcnn_resnet101_coco_2017_11_08'
    MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_oid_2017_11_08'

    MODEL_FILE = MODEL_NAME + '.tar.gz'
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

    # List of the strings that is used to add correct label for each box.
    # PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
    PATH_TO_LABELS = os.path.join('data', 'oid_bbox_trainable_label_map.pbtxt')
    NUM_CLASSES = 545

    # Size, in inches, of the output images.
    IMAGE_SIZE = (12, 8)

    def __init__(self, path_to_labels=None, num_classes=None):
        self.detection_graph = tf.Graph()

        if path_to_labels:
            self.PATH_TO_LABELS = path_to_labels
        if num_classes:
            self.NUM_CLASSES = num_classes

        # load label_map
        self.label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        self.categories = label_map_util.convert_label_map_to_categories(self.label_map,
                                                                         max_num_classes=self.NUM_CLASSES,
                                                                         use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)

    # Download Model
    def download_model(self):
        opener = urllib.request.URLopener()
        opener.retrieve(self.DOWNLOAD_BASE + self.MODEL_FILE, self.MODEL_FILE)
        tar_file = tarfile.open(self.MODEL_FILE)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, os.getcwd())

    # Load a (frozen) Tensorflow model into memory.
    def load_frozen_model(self):
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

    @staticmethod
    def load_image_into_numpy_array(image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def view_img(self, image, boxes, classes, scores):
        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8)

        plt.figure(figsize=self.IMAGE_SIZE)
        plt.imshow(image)
        pylab.show()

    # the id & path of image must be given
    def run_detection(self, path_list, show_res=False):
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Definite input and output Tensors for detection_graph
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                for path in path_list:
                    try:
                        image = Image.open(path)
                        # the array based representation of the image will be used later in order to prepare the
                        # result image with boxes and labels on it.
                        image_np = self.load_image_into_numpy_array(image)
                        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                        image_np_expanded = np.expand_dims(image_np, axis=0)
                        # Actual detection.
                        (boxes, scores, classes, num) = sess.run(
                            [detection_boxes, detection_scores, detection_classes, num_detections],
                            feed_dict={image_tensor: image_np_expanded})

                        result = [{'score': float(x), 'class_id': int(y), 'class': self.category_index[y]['name']} for
                                  x, y
                                  in
                                  zip(
                                      scores[0], classes[0]) if x > 0.5]

                        # Visualization of the results of a detection.
                        if show_res:
                            self.view_img(image_np, boxes, classes, scores)
                        yield path, result
                    except:
                        yield path, None


def quick_detection(path):
    detector = ObjectDetector()
    detector.load_frozen_model()
    statistics = {}
    path_list = [path]
    for p in detector.run_detection(path_list):
        res = p[1]
        if res:
            detected_class = set([x['class'] for x in res])
            print(detected_class)
            for class_x in detected_class:
                if class_x in statistics:
                    statistics[class_x] += 1
                else:
                    statistics[class_x] = 1
    ret = sorted(statistics.items(), key=lambda item: item[1], reverse=True)
    return ret


def mongo_process():
    conn = pymongo.MongoClient('127.0.0.1', 27017)
    db = conn.flickr_db  # 连接flickr_db数据库，没有则自动创建
    set_name = 'sadness'
    emo_set = db[set_name]

    detector = ObjectDetector()
    detector.load_frozen_model()

    images = {}
    for data in emo_set.find():
        id = data.get('id')
        url = data.get('url')
        path = 'trainset/' + set_name + '/' + url.split('/')[4]
        if os.path.exists(path):
            images[path] = id

    print(f'total:{len(images.keys())}')
    valid_count = 0
    statistics = {}
    for p in detector.run_detection(images.keys()):
        path = p[0]
        res = p[1]
        if res:
            valid_count += 1
            detected_class = set([x['class'] for x in res])
            print(detected_class)
            for class_x in detected_class:
                if class_x in statistics:
                    statistics[class_x] += 1
                else:
                    statistics[class_x] = 1
        emo_set.update({'id': images[path]}, {'$set': {'objects_contained_oid': res}})
    print(sorted(statistics.items(), key=lambda item: item[1], reverse=True))
    print(f'valid:{valid_count}')


if __name__ == '__main__':
    res = quick_detection('trainset/6362320846773172484137057.jpg')
    # print(res)
    # mongo_process()
    pass
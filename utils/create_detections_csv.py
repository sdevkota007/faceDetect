# import the necessary packages
import numpy as np
import tensorflow as tf
import cv2 as cv
import os
from imutils import paths

# Read the graph.
val_images = "../data/images/test/WIDER_val/images"

det_folder = "../metrics/Object-Detection-Metrics/detections-faces"
'''
output detection file should have the format
face .88 5 67 31 48
'''

with tf.gfile.FastGFile('../trained-inference-graphs/output_inference_graph_v1.pb/frozen_inference_graph.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

with tf.Session() as sess:
    # Restore session
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')


    # grab the paths to the input images
    imagePaths = list(paths.list_images(val_images))
    print(len(imagePaths))

    for imagePath in imagePaths:
        # Read and preprocess an image.
        img = cv.imread(imagePath)
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

        # Run the model
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                        sess.graph.get_tensor_by_name('detection_scores:0'),
                        sess.graph.get_tensor_by_name('detection_boxes:0'),
                        sess.graph.get_tensor_by_name('detection_classes:0')],
                       feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        # Visualize detected bounding boxes.
        num_detections = int(out[0][0])
        if num_detections == 0:
            print("Could not find detections for {}")
        for i in range(num_detections):
            classId = int(out[3][0][i])
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.5:
                xmin = int( bbox[1] * cols )
                ymin = int( bbox[0] * rows )
                xmax = int( bbox[3] * cols )
                ymax = int( bbox[2] * rows )
                # cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)

            out_file = imagePath.split("/")[-1].split(".")[0] + ".txt"
            class_name = "face"

            content = "{0} {1} {2} {3} {4} {5}\n".format(class_name, score, xmin, ymin, xmax, ymax)
            out_file = os.path.join(det_folder, out_file)
            with open(out_file, 'a+') as f:
                f.write(content)

# cv.imshow('TensorFlow MobileNet-SSD', img)
# cv.waitKey()






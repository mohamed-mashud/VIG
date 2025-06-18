import cv2
import time
from picamera2 import Picamera2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

model = 'efficientdet_lite0.tflite'
num_threads = 4

dispW = 500
dispH = 500

picam2 = Picamera2()
picam2.preview_configuration.main.size=(dispW,dispH)
picam2.preview_configuration.main.format = 'RGB888'
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

pos=(20,60)
font = cv2.FONT_HERSHEY_SIMPLEX
height = 1.5
weight = 3
myColor =(255,0,0)

fps = 0

base_options= core.BaseOptions(file_name=model,use_coral=False,num_threads= num_threads)
detection_options=processor.DetectionOptions(max_results=8, score_threshold=.3)
options = vision.ObjectDetectorOptions(base_options= base_options,detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)

while True:
    #ret, im = cam.read()
    im = picam2.capture_array()
    im = cv2.flip(im,-1)
    imRGB = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    imTensor=vision.TensorImage.create_from_array(imRGB)
    detections = detector.detect(imTensor)
    image = utils.visualize(im,detections)
    cv2.imshow('Camera',im)
    if cv2.waitKey(1)==ord('q'):
        break
    
cv2.destroyAllWindows()
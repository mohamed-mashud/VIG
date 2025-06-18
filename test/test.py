import cv2
import pytesseract
from pytesseract import Output
from picamera2 import Picamera2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

##cap = cv2.VideoCapture(0)
##cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

dispW = 1280
dispH = 720

model = 'efficientdet_lite0.tflite'
num_threads = 4

picam2 = Picamera2()
picam2.preview_configuration.main.size=(dispW,dispH)
picam2.preview_configuration.main.format = 'RGB888'
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

base_options= core.BaseOptions(file_name=model,use_coral=False,num_threads= num_threads)
detection_options=processor.DetectionOptions(max_results=8, score_threshold=.3)
options = vision.ObjectDetectorOptions(base_options= base_options,detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)

while True:
    # Captura de im por im
    ##ret, im = cap.read()
    im = picam2.capture_array()
    im = cv2.flip(im,-1)
    d = pytesseract.image_to_data(im)
    print(d)
    txt_box = len(d[""])
    for i in range(txt_box):
    # Procesar solo con nivel de confianza mayor a 60 %
        if int(d['conf'][i]) > 60:
            (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # no mostrar texto vacio
            if text and text.strip() != "":
                im = cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                im = cv2.putText(im, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
 
    # Abre ventana y muestra resultado
    cv2.imshow('Camera', im)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows() 
import cv2
import numpy as np
import pytesseract
from picamera2 import Picamera2

# Initialize the camera

dispW = 500
dispH = 500

picam2 = Picamera2()
picam2.preview_configuration.main.size=(dispW,dispH)
picam2.preview_configuration.main.format = 'RGB888'
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Wait for the camera to warm up (optional)
import time
time.sleep(2)

# Function to extract text from an image using Tesseract
def extract_text_from_image(im):
    # Convert the image to grayscale
    im = picam2.capture_array()
    im = cv2.flip(im,-1)
    imRGB = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)

    # Perform OCR (text recognition) using Tesseract
    text = pytesseract.image_to_string(imRGB)

    return text
while True:
    #ret, im = cam.read()
    im = picam2.capture_array()
    im = cv2.flip(im,-1)
    imRGB = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    print(extract_text_from_image(imRGB))
    #imTensor=vision.TensorImage.create_from_array(imRGB)
    #detections = detector.detect(imTensor)
    #image = utils.visualize(im,detections)
    cv2.imshow('Camera',im)
    if cv2.waitKey(1)==ord('q'):
        break
# Main loop
    # You can add more logic here, like saving the frames or performing other actions
    
    # Exit the loop if needed
    # if some_condition:
    #     break

# Release the camera resource
#if cv2.waitKey(1)==ord('q'):
        #break#
cv2.destroyAllWindows()


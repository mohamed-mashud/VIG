import picamera
import pytesseract

# Initialize the camera module
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30

# Start a loop to continuously capture and process frames
while True:
    # Capture a frame from the camera
    frame = camera.capture()

    # Convert the frame to a PIL image
    image = frame.convert('RGB')

    # Extract text blocks from the image
    data = pytesseract.image_to_data(image, config='--oem 3 --psm 6')

    # Iterate through the list of text blocks and extract the text
    for block in data.splitlines():
        text = block[1:-1]
        if len(text) > 0:
            print(text)

    # Release the camera resources
    camera.close()

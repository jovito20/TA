import time
import os
import cv2

def gstreamer_pipeline(
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def capture(index):
    # Capture image from laptop webcam
    image_name = 'image_{}.jpg'.format(index)
    print("Capturing and saving image as:", image_name)
    camera = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    ret, frame = camera.read()
    camera.release()
   
    if ret:
        # Save the image locally with the generated file name
        cv2.imwrite(image_name, frame)
        print("Image saved locally.")
    else:
        print("Failed to capture image.")
# Call the function to capture image and upload to Firebase
for i in range(10):
    capture(i)  # Call the function
    
    time.sleep(5)  # Delay for 5 seconds

    if i == 9:  # Check if this is the 10th iteration
        print("Limit reached. Exiting loop.")
        break  # Exit the loop after 10 iterations

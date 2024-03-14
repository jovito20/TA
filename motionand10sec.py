import cv2
import time
import os
from ultralytics import YOLO


# Initialize the camera
cap = cv2.VideoCapture(0)

# Define motion detection parameters
threshold = 30  # Threshold for detecting motion
min_contour_area = 500  # Minimum contour area for motion detection

# Initialize variables
prev_frame = None
prev_time = time.time()
capture_interval = 10  # Capture image every 10 seconds
save_dir = "saved_picture"  # Specify the directory to save images

# Create the directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

while True:
    # Read frame from camera
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Blur the frame to reduce noise
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    if prev_frame is None:
        prev_frame = blurred_frame
        continue

    # Calculate absolute difference between current frame and previous frame
    frame_diff = cv2.absdiff(prev_frame, blurred_frame)
    
    # Apply a threshold to the frame difference
    _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Check if any contour meets minimum area requirement
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            # Motion detected
            
            image_path = os.path.join(save_dir, f"captured_image_{int(curr_time)}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Motion detected! Image saved to: {image_path}")
            prev_time = curr_time

            #detect
            # source=image_path
            # model = YOLO('best.pt')
            # model.predict(source=source, save=True, conf=0.5)
            # os.remove(image_path)
            #jeda 3 detik
            

    # Update previous frame
    prev_frame = blurred_frame

    # Check if it's time to capture image
    curr_time = time.time()
    if curr_time - prev_time >= capture_interval:
        # Save the image to specified directory
        image_path = os.path.join(save_dir, f"captured_image_{int(curr_time)}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Image saved to: {image_path}")
        prev_time = curr_time
        #for detect
        source=image_path
        model = YOLO('best.pt')
        model.predict(source=source, save=True, conf=0.5)
        # os.remove(image_path)


    # Display the frame
    cv2.imshow("Camera Feed", frame)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

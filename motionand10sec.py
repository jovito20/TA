# Object detection using a single camera sensor (stable)

import cv2
from ultralytics import YOLO
import os

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

def spc_detect():
    threshold = 30  # Threshold for detecting motion
    min_contour_area = 500  
    prev_frame = None
    prev_time = time.time()
    capture_interval = 10  # Capture image every 10 seconds
    save_dir = "saved_picture"  # Specify the directory to save images
    window_title = "Smart Cart"
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    motion_direction = None
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if video_capture.isOpened():
        try:
            cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret, frame = video_capture.read()

                if not ret:
                    break

                # Convert frame to grayscale for motion detection
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)  # Apply Gaussian blur to reduce noise

                if prev_frame is None:
                    prev_frame = blurred_frame
                    continue

                # Calculate the absolute difference between the current frame and the previous frame
                frame_delta = cv2.absdiff(prev_frame, blurred_frame)
                _, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
                

                # Find contours of moving objects
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

                prev_frame = blurred_frame    

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


                # Display the frames and motion direction
                
                cv2.imshow(window_title, frame)

                # Exit by pressing 'Q'
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    spc_detect()

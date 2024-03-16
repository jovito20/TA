import cv2
import threading
import shutil
import time

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

def take_picture_with_preview(output_file='test1'):
    """
    Take a picture using the default camera with a 3-second delay and preview the camera feed.

    :param output_file: The name of the output file (including path if needed).
    """
    # Open the default camera
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

    # Set the resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    
        # Create a window to display the camera feed
    cv2.namedWindow('Camera Feed', cv2.WINDOW_AUTOSIZE)

    try:
        # Delay for 3 seconds
        #time.sleep(3)

        # Loop to display the camera feed
        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Check if the frame was read correctly
            if ret:
                # Display the frame in the window
                cv2.imshow('Camera Feed', frame)

                # Wait for a key press and exit the loop if the 'q' key is pressed
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Release the camera resources
        cap.release()

        # Save the last frame as an image file
        cv2.imwrite(output_file, frame)

    finally:
        # Close all OpenCV windows
        cv2.destroyAllWindows()

# Example usage
take_picture_with_preview('my_image9.jpg')

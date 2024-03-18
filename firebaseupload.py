import cv2
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

def upload_to_firebase(image_name):
    try:
        # Upload image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(image_name)
        blob.upload_from_filename(image_name)

        print(f"Image uploaded to Firebase Storage: {blob.public_url}")
        return True
    except Exception as e:
        print(f"Error uploading image to Firebase Storage: {e}")
        return False

def capture_and_upload_image():
    # Capture image from laptop webcam
    camera = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    ret, frame = camera.read()
    camera.release()

    if ret:
        # Save image locally
        image_name = 'test.jpg'
        cv2.imwrite(image_name, frame)
        print("Image captured successfully.")

        # Upload image to Firebase
        if upload_to_firebase(image_name):
            # Remove local image file after uploading
            os.remove(image_name)
            print("Local image file removed.")
        else:
            print("Failed to upload image. Local file not removed.")
    else:
        print("Failed to capture image.")

# Call the function to capture image and upload to Firebase
capture_and_upload_image()

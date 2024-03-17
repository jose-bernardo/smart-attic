import cv2
import time
import requests
import os

def main():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    # Record for 5 seconds
    end_time = time.time() + 5

    # Capture video frames and save to file
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

        if time.time() > end_time:
            break

    # Release the camera and close the video file
    cap.release()
    out.release()

    # Send the video file via HTTP POST request
    url = 'http://' + (os.getenv('SERVER_URL') or "127.0.0.1:5001") + '/add-footage'
    files = {'video': open('output.avi', 'rb')}
    response = requests.post(url, files=files)

    # Print response
    print(response.text)

if __name__ == "__main__":
    main()

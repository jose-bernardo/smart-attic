import cv2
import time
import requests
import os
import sys

def main():
    server_url = os.getenv("SERVER_URL") or "127.0.0.1:5001"
    server_url = 'http://' + server_url if not server_url.startswith('http://') else server_url

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
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

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
    files = {'video': open('output.mp4', 'rb')}
    data = {'username': sys.argv[1], 'status': sys.argv[2]}
    response = requests.post(server_url + '/addFootage', data=data, files=files)
    os.remove('output.mp4')

    # Print response
    print(response.text)

if __name__ == "__main__":
    main()

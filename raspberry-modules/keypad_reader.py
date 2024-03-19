import requests
import os
import subprocess
import serial

server_url = os.getenv('SERVER_URL') or '127.0.0.1:5001'
server_url = 'http://' + server_url if not server_url.startswith('http://') else server_url

serial_ports = {'user1': os.getenv("SERIAL_PORT")}
baud_rate = 9600

def read_input():
    # Read exactly 1 digit
    while True:
        digit1 = input("Enter your ID: ")
        if digit1.isdigit() and len(digit1) == 1:
            break
        else:
            print("Invalid input. Please enter exactly 1 digit.")

    # Read exactly 4 digits
    while True:
        digits = input("Enter the 4 digt PIN: ")
        if digits.isdigit() and len(digits) == 4:
            break
        else:
            print("Invalid input. Please enter exactly 4 digits.")

    return digit1, digits

if __name__ == "__main__":

    while(True):
        userid, pin = read_input()

        data = {'userid': 'user' + userid, 'pin': pin}
        response = requests.post(server_url + '/enterPin', data=data)

        if response.ok:
            print(response.text)  # Print the raw response content
            
            ser = serial.Serial(serial_ports['user1'], baud_rate)
            ser.write("door".encode())
            ser.write(b'\n')

            if (response.text != "Access granted."):
                #TODO send red light to the led
                ser.write("close".encode())
                ser.write(b'\n')
                subprocess.Popen(["python3", "camera.py", userid]).wait()
            
            else:
                ser.write("open".encode())
                ser.write(b'\n')
            
            ser.close()

        else:
            print("Failed to get a valid response from the server.")

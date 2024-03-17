import requests
import subprocess

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
        
        url = 'http://127.0.0.1:5001/enterPin'  # Replace 'your-api-endpoint' with the actual endpoint
        data = {'userid': 'user' + userid, 'pin': pin}
        response = requests.post(url, data=data)
        
        if response.ok:
            print(response.text)  # Print the raw response content
            #TODO send green light to the led

            if (response.text != "Access granted."):
                #TODO send red light to the led
                subprocess.Popen(["python3", "camera.py"]).wait()

        else:
            print("Failed to get a valid response from the server.")

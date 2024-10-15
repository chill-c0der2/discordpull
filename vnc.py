import socket
import pickle
import cv2
import numpy as np
import pyautogui

def send_control_data(sock, command):
    sock.sendall(pickle.dumps(command))

def start_client():
    server_ip = '192.168.0.145'  # Hard-coded server IP address
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Attempt to connect to the server
    try:
        client.connect((server_ip, 9999))  # Connect back to the server's IP
        print(f"Connected to server at {server_ip}")
    except Exception as e:
        print(f"Failed to connect to server at {server_ip}: {e}")
        return

    while True:
        # Receive screen size and image
        screen_size = pickle.loads(client.recv(4096))
        screen_data = b""
        while len(screen_data) < screen_size:
            screen_data += client.recv(screen_size - len(screen_data))

        # Convert bytes back to image and display
        nparr = np.frombuffer(screen_data, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow('Remote Desktop', img_np)

        # Capture local input and send to the server
        x, y = pyautogui.position()
        send_control_data(client, {'type': 'move_mouse', 'x': x, 'y': y})

        # Keyboard input example (for demonstration)
        key = cv2.waitKey(1)
        if key != -1:
            send_control_data(client, {'type': 'keypress', 'key': chr(key)})

        # Break the loop if the window is closed
        if cv2.getWindowProperty('Remote Desktop', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_client()

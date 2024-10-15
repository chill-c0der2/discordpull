import socket
import cv2
import numpy as np
import pickle
import struct
import pyautogui

def start_client():
    server_ip = '8.tcp.ngrok.io'  # Your Ngrok address
    server_port = 10305  # Your Ngrok port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    while True:
        # Receive the screen data
        data = b""
        while len(data) < struct.calcsize("L"):
            packet = client.recv(4096)
            if not packet:
                print("No packet received, exiting...")
                return  # Exit if no more packets are received
            data += packet
        msg_size = struct.unpack("L", data[:struct.calcsize("L")])[0]
        data = data[struct.calcsize("L"):]

        while len(data) < msg_size:
            packet = client.recv(4096)
            if not packet:
                print("No more data received, exiting...")
                return  # Exit if no more packets are received
            data += packet

        # Decode the image
        try:
            frame = pickle.loads(data)
            # Display the image
            cv2.imshow("Remote Desktop", frame)

            # Handle mouse control
            x, y = pyautogui.position()
            command = f"move,{x},{y}"
            client.send(command.encode('utf-8'))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error decoding frame: {e}")
            break

    client.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_client()

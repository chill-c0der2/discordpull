import socket
import pickle
from PIL import Image
import io

def start_client():
    server_ip = '8.tcp.ngrok.io'  # Replace with your Ngrok address
    server_port = 10305  # Replace with your Ngrok port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        while True:
            # Receive the size of the image
            img_size_data = client.recv(4096)
            if not img_size_data:
                break
            
            img_size = pickle.loads(img_size_data)

            # Receive the actual image data
            img_data = b''
            while len(img_data) < img_size:
                packet = client.recv(4096)
                if not packet:
                    break
                img_data += packet

            # Convert the byte data back to an image
            img = Image.open(io.BytesIO(img_data))
            img.show()  # Display the image (this may open a new window each time)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    start_client()

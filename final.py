import requests
import cv2
import numpy as np
import pickle

def start_client():
    server_url = 'https://1fa6-79-134-141-41.ngrok-free.app/screen'  # Your Ngrok HTTP URL

    while True:
        try:
            # Request the latest screen
            response = requests.get(server_url)
            if response.status_code == 200:
                # Decode the image
                frame = pickle.loads(response.content)

                # Display the image
                cv2.imshow("Remote Desktop", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print(f"Failed to get image: {response.status_code}")
        except Exception as e:
            print(f"Error in client: {e}")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_client()

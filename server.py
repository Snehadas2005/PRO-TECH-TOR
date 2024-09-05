import socket
import os
import time

def send_images(image_paths, host='10.10.219.155', port=12345):
    for image_path in image_paths:
        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            # Send the length of the image data followed by the image data itself
            image_length = len(image_data)
            client_socket.sendall(image_length.to_bytes(4, byteorder='big'))  # Send the length as 4 bytes
            client_socket.sendall(image_data)
            print(f"Image {image_path} sent successfully")

            client_socket.close()
            time.sleep(1)  # Sleep for 1 second between sending images

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    image_paths=["face_0.jpg","face_1.jpg","face_2.jpg","face_3.jpg"]
    (send_images
     (image_paths, host='10.10.219.155', port=12345))


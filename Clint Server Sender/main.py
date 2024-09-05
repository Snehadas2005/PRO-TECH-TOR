import socket
import os

def start_server(host='10.10.202.174', port=12345, save_directory='received_images'):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    image_count = 0
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        while True:
            try:
                # Receive the length of the image data
                length_data = client_socket.recv(4)
                if not length_data:
                    print("Connection closed by the client.")
                    break  # Exit the loop if no data is received (connection closed)
                
                image_length = int.from_bytes(length_data, byteorder='big')

                # Receive the image data based on the length
                image_data = b''
                while len(image_data) < image_length:
                    packet = client_socket.recv(image_length - len(image_data))
                    if not packet:
                        print("Connection lost while receiving image data.")
                        break
                    image_data += packet
                
                if image_data:
                    # Save the received image data
                    if image_data.endswith(".jpg"):
                        image_filename = os.path.join(save_directory, f"image_{image_count}.jpg")
                    elif image_data.endswith(".avi"):
                        image_filename = os.path.join(save_directory, f"image_{image_count}.avi")
                    elif image_data.endswith(".wav"):
                        image_filename = os.path.join(save_directory, f"image_{image_count}.wav")
                    else:
                        image_filename = os.path.join(save_directory, f"image_{image_count}.xml")
                    
                    with open(image_filename, 'wb') as image_file:
                        image_file.write(image_data)
                    
                    print(f"Image saved as {image_filename}")
                    image_count += 1

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        client_socket.close()


if __name__ == "__main__":
    start_server()

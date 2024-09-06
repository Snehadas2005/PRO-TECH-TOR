import socket
import os

def start_target_server(host='192.168.174.50', port=54321, save_directory='forwarded_files'):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Target server listening on {host}:{port}")

    file_count = 0
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        while True:
            try:
                # Receive the length of the metadata
                metadata_length_data = client_socket.recv(4)
                if not metadata_length_data:
                    print("Connection closed by the client.")
                    break

                metadata_length = int.from_bytes(metadata_length_data, byteorder='big')

                # Receive the metadata (file name and size)
                metadata = client_socket.recv(metadata_length).decode()
                file_name, file_length = metadata.split(',')
                file_length = int(file_length)

                # Receive the actual file data
                file_data = b''
                while len(file_data) < file_length:
                    packet = client_socket.recv(file_length - len(file_data))
                    if not packet:
                        print("Connection lost while receiving file data.")
                        break
                    file_data += packet

                # Save the forwarded file
                if file_data:
                    file_path = os.path.join(save_directory, file_name)
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
                    
                    print(f"File {file_name} saved successfully at {file_path}.")
                    file_count += 1

            except Exception as e:
                print(f"An error occurred while processing the forwarded file: {e}")
                break

        client_socket.close()

if __name__ == "__main__":
    start_target_server()

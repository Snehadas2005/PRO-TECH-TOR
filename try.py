import socket
import os

def start_server(host='192.168.174.41', port=12345, save_directory='received_files'):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(5)
            print(f"Server listening on {host}:{port}")

            file_count = 0
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connected to {client_address}")

                while True:
                    try:
                        # Receive the length of the metadata (file type and length)
                        metadata_length_data = client_socket.recv(4)
                        if not metadata_length_data:
                            print("Connection closed by the client.Server is Active.....")
                            break
                        
                        metadata_length = int.from_bytes(metadata_length_data, byteorder='big')
 
                        # Receive the metadata (file type and file size)
                        metadata = client_socket.recv(metadata_length).decode()
                        file_type, file_length = metadata.split(',')
                        file_length = int(file_length)

                        # Receive the actual file data
                        file_data = b''
                        while len(file_data) < file_length:
                            packet = client_socket.recv(file_length - len(file_data))
                            if not packet:
                                print("Connection lost while receiving file data.")
                                break
                            file_data += packet
                        
                        if file_data:
                            # Determine file extension based on the file type
                            if file_type == 'image':
                                file_extension = 'jpg'
                            elif file_type == 'audio':
                                file_extension = 'mp3'
                            elif file_type == 'video':
                                file_extension = 'mp4'
                            else:
                                print("Unknown file type.")
                                break
                            
                            # Save the received file
                            file_filename = os.path.join(save_directory, f"file_{file_count}.{file_extension}")
                            with open(file_filename, 'wb') as file:
                                file.write(file_data)
                            
                            print(f"{file_type.capitalize()} saved as {file_filename}")
                            file_count += 1

                    except Exception as e:
                        print(f"An error occurred while processing a client: {e}")
                        break

                client_socket.close()

        except Exception as e:
            print(f"Server encountered an error and will restart: {e}")
            server_socket.close()

if __name__ == "__main__":
    start_server()

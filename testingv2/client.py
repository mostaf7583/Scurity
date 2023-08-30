import requests
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import rsa




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


def send_encypted_key(data):
    response = requests.post('http://127.0.0.1:12345/receive_data', data={'data': data})
    return response.text

def receive_public_key():
    response = requests.get(' http://127.0.0.1:12345/send_public_key')
    return response.text

def encrypt_key(key, public_key):
    # convert the public key to an rsa object
    public_key = rsa.PublicKey.load_pkcs1(public_key)
    cipher_rsa = rsa.encrypt(key, public_key)
    return cipher_rsa

if __name__ == "__main__":
    key_original  = generate_key()
    
    public_key = receive_public_key()
    key_encrypted = encrypt_key(key_original , public_key)
    response = send_encypted_key(key_encrypted )
    print("Server Response:", response)

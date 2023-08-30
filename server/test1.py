import socket
import threading
import rsa








def generate_key_pair():
    (public_key, private_key) = rsa.newkeys(512)
    return public_key, private_key
# Save the keys to files A

def handle_client(client_socket, private_key):
    received_key = client_socket.recv(4096)  # Receiving the encrypted key
    cipher_rsa = rsa.decrypt(received_key, private_key)
    decrypted_key = cipher_rsa.decrypt(received_key)
    
    print(f"Decrypted key: {decrypted_key.decode()}")
    
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Received from client: {data}")
        response = f"Server received: {data}"
        client_socket.send(response.encode())
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    private_key, public_key = generate_key_pair()

    print("Server is listening...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_socket.send(public_key.save_pkcs1())
        print(f"Connection established with {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,private_key))
        client_thread.start()

if __name__ == "__main__":
    start_server()

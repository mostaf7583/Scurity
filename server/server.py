import socket
import rsa

SERVER_IP = 'localhost'
SERVER_PORT = 11000

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn,addr = s.accept()
    print(f'Connection accepted from :{addr}')
    with conn:
        while(True):
            conn.send(b'Hello World')
            key =  conn.recv(1024)
            print(key)
            break
#  Generate a Public/Private key-pair using RSA ( server side)
(public_key, private_key) = rsa.newkeys(512)
# Save the keys to files A
with open('public.pem', 'wb') as f:
    f.write(public_key.save_pkcs1())
with open('private.pem', 'wb') as f:
    f.write(private_key.save_pkcs1())

#send the public key to the client

with open('public.pem', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
    print(public_key)
    # convert the public key to be bytes like object
    newpupkey=public_key.save_pkcs1()
    print(newpupkey)
    conn.send(newpupkey)
    # print('public key sent')
    # f.close() 
    # conn,addr = s.accept()
    # print(f'Connection accepted from :{addr}')
    # with conn:
    #     while(True):
    #         conn.send(newpupkey)
    #         break
    
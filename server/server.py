import socket

SERVER_IP = 'localhost'
SERVER_PORT = 5678

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn,addr = s.accept()
    print(f'Connection accepted from :{addr}')
    with conn:
        while(True):
            conn.send(b'Hello World')
            data =  conn.recv(1024)
            print(data)
            break

# save the received key in key.key file
with open('key.key', 'wb') as f:
    f.write(data)
# end the connection



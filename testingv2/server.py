from flask import Flask, request
import rsa

app = Flask(__name__)


def generate_key_pair():
    (public_key, private_key) = rsa.newkeys(512)
    return public_key, private_key

public_key, private_key = generate_key_pair()


@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.form.get('data')
    print("Received:", data)
    return "Data received by server!"


@app.route('/send_public_key', methods=['GET'])
def send_public_key():
    return public_key.save_pkcs1()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)

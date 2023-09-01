import rsa
def generate_key_pair():
    (public_key, private_key) = rsa.newkeys(512)
    return public_key, private_key

public_key, private_key = generate_key_pair()

# encrypt the message with the public key
message = 'Hello World!'
message = message.encode('utf8')
encrypted_message = rsa.encrypt(message, public_key)
print(message)

# decrypt the message with the private key
decrypted_message = rsa.decrypt(encrypted_message, private_key)
decrypted_message = decrypted_message.decode('utf8')

print(decrypted_message)





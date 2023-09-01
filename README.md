Creating a block diagram for your encryption and decryption process can be an excellent way to visually represent the flow of data and functions in your system. I'll describe the structure and components, and you can use this information to create the diagram using a suitable diagramming tool or software.

**Block Diagram for Encryption and Decryption:**

Here's a textual representation of the block diagram:

```
    +--------------------------------+
    |          Client (client.py)    |
    +--------------------------------+
               |       |       |
               |       |       |
          +---------+  |  +---------+
          | Encrypt |  |  | Decrypt |
          +---------+  |  +---------+
               |       |       |
               |       |       |
    +--------------------------------+
    |   Web Server (server.py)   |
    +--------------------------------+
               |       |       |
               |       |       |
          +---------+  |  +---------+
          |   Key   |  |  |   Key   |
          | Exchange|  |  |  Exchange|
          +---------+  |  +---------+
               |       |       |
               |       |       |
    +--------------------------------+
    |        RSA Cryptography       |
    +--------------------------------+
               |       |       |
               |       |       |
    +---------+  |  +---------+  +---------+
    |   Fernet|  |  | RSA    |  | Fernet  |
    |  Encryption|  |  Key    |  | Decryption|
    +---------+  |  |  Pair  |  +---------+
               |       |       |
               |       |       |
    +---------+  |  +---------+
    |    AES  |  |  |    AES  |
    |  Encryption|  |  | Decryption|
    +---------+  |  +---------+
               |       |
               |       |
    +---------+  +---------+
    | File  |  | File  |
    | I/O   |  | I/O   |
    +---------+  +---------+
```

**Components and Functions:**

1. **Client (client.py):**
   - Manages the encryption and decryption process for files and folders.
   - Communicates with the server to exchange keys and make payments.

2. **Web Server (server.py):**
   - Serves as the server-side component.
   - Handles key exchange and payment requests from the client.

3. **RSA Cryptography:**
   - Performs asymmetric encryption and decryption.
   - Generates public and private key pairs.
   - Encrypts and decrypts the symmetric encryption key.

4. **Fernet Encryption/Decryption:**
   - Performs symmetric encryption and decryption using the AES algorithm with a Fernet key.

5. **AES Encryption/Decryption:**
   - Symmetric encryption and decryption using the Advanced Encryption Standard (AES) algorithm.
   - Encrypts and decrypts file data.

6. **File I/O:**
   - Reads and writes data to/from files.

**Flow of Operations:**

1. The client generates a symmetric encryption key (Fernet key) using `generate_key()`.

2. It encrypts files and folders using the Fernet key with `encrypt_file()` and `encrypt_folder_recursive()` functions. Original files are deleted after encryption.

3. The client requests the public key from the server using `send_public_key()`.

4. The client encrypts the Fernet key with the server's public key using `encrypt_key()`.

5. The encrypted Fernet key is sent to the server using `send_encypted_key()`.

6. The server decrypts the Fernet key using RSA private key using `decrypt_key()`.

7. The client may make a payment using `send_payment()`, which is received by the server.

8. The client decrypts files and folders using the decrypted Fernet key with `decrypt_folder_recursive()`. Encrypted files are deleted after decryption.


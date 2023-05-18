import os
import getpass
from cryptography.fernet import Fernet

# get the user's home directory
home_dir = os.path.expanduser("~")

# specify the path to the root directory to iterate through
root_dir = os.path.join(home_dir, "Documents")

# generate a Fernet key for AES encryption
key = Fernet.generate_key()

# create a Fernet object with the generated key
fernet = Fernet(key)

# recursively loop through all files and subdirectories within the root directory
for root, dirs, files in os.walk(root_dir):
    for file in files:
        # get the full path to the file
        file_path = os.path.join(root, file)

        # encrypt the file and write it to a new encrypted file
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted_data = fernet.encrypt(data)
        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, "wb") as f:
            f.write(encrypted_data)

    for dir in dirs:
        # create an encrypted subdirectory with the same name as the original subdirectory
        orig_dir_path = os.path.join(root, dir)
        encrypted_dir_path = os.path.join(root, fernet.encrypt(dir.encode()).decode())
        os.mkdir(encrypted_dir_path)

        # recursively loop through all files within the original subdirectory and encrypt them
        for subdir_root, subdir_dirs, subdir_files in os.walk(orig_dir_path):
            for subdir_file in subdir_files:
                # get the full path to the file
                subdir_file_path = os.path.join(subdir_root, subdir_file)

                # encrypt the file and write it to a new encrypted file in the encrypted subdirectory
                with open(subdir_file_path, "rb") as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                encrypted_file_path = os.path.join(subdir_file_path + ".encrypted")
                with open(encrypted_file_path, "wb") as f:
                    f.write(encrypted_data)


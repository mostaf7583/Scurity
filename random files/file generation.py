# genrate randrom txt files and fill them wit h ipsum upsum and put them in the folder in afolder named random files 



import os
import random
import string

# Create a folder for random files
folder_name = "random files"
os.makedirs(folder_name, exist_ok=True)

# Number of random files to generate
num_files = 10

# Generate and save random text files
for i in range(num_files):
    # Generate random file name
    file_name = ''.join(random.choices(string.ascii_lowercase, k=8)) + ".txt"
  
    # Generate random "Lorem ipsum" text
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas dictum, lorem vitae consequat iaculis, neque purus dapibus lectus, sed fermentum ex ex ut risus."
  
    # Save the random text to a file
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "w") as file:
        file.write(lorem_ipsum)
        

    print(f"Created file: {file_name}")

print("Random text files have been generated and saved in the 'random files' folder.")
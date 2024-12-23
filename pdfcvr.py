from pathlib import Path
from time import sleep
import sys
import os
import secrets

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PILLOW library not installed yet on your python.")
    ch = input("Do you want install PILLOW python's library (y/N) ").lower()
    if ch == "y":
        os.system("pip install pillow")
    else:
        sys.exit("You can't run this tool without PILLOW library installed.")

# Essential Variable
max_images = 20

help = r'''
  ____     _  __  ____
 |  _ \ __| |/ _|/ ___|_   ___ __
 | |_) / _` | |_| |   \ \ / / '__|
 |  __/ (_| |  _| |___ \ V /| |
 |_|   \__,_|_|  \____| \_/ |_|
  Github  : github.com/hakimdaniel
  Version : Python 3.12.8

      Images to pdf converter

[Information]

- Just enter blank for proceed images
- Make sure your images in same folder,
  so this program will found your file
- Your output will saved same path of this program
- File output renamed as output_<random>.pdf
- RGBA/Transparent images not support
- Max images just 20 default for decrease lagging,
  you can edit code at  variable "max_images" for
  more value
'''

images = []
bil = 0

print(help)

# Dapatkan direktori skrip semasa
script_directory = os.path.dirname(os.path.realpath(__file__))

# Senaraikan semua fail gambar dalam direktori yang sama dengan skrip
image_extensions = ('.jpg', '.jpeg', '.png', '.pdf')
image_files = [f for f in os.listdir(script_directory) if f.lower().endswith(image_extensions)]

if not image_files:
    sys.exit("No image files detected in the current directory.")

print("Images file detected:")
for file in image_files:
    print("[+] " + file)

print("\nType \"exit\" for abort and cancel process.")
while len(images) < max_images:
    bil += 1
    add = input(f"=> Gambar {bil} : ")
    if add.lower() == "exit":
        sys.exit("Abort program from running.")
    if add and not Path(add).is_file():
        # check file list
        sys.exit(f"File \"{add}\" is not found in your path.")
    if add and not add.lower().endswith(image_extensions):
        sys.exit(f"File \"{add}\" is not a supported image format.")
    if add:
        images.append(add)
    else:
        break

# check if images inserted
if not images:
    sys.exit("No images selected.")

# Output name
pdf_path = "output_" + secrets.token_hex(3) + ".pdf"

try:
    # to convert image into RGB type
    image1 = Image.open(images[0]).convert('RGB')
    image_list = [Image.open(img).convert('RGB') for img in images[1:]]

    # Simpan ke PDF
    image1.save(pdf_path, save_all=True, append_images=image_list)
    print(f"PDF saved as {pdf_path}")
except Exception as e:
    sys.exit(f"Error occurred: {e}")

sleep(2)

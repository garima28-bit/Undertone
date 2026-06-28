import os                                         # OS Library for File handling
from PIL import Image                             # Pillow Library for Image Handling

word = input("Please enter the word or phrase you wish to hide! - ")                    # Input for the word/phrase to be hidden in the image

base_dir = os.path.dirname(os.path.abspath(__file__))                                   # Takes the file location
img = Image.open(os.path.join(base_dir, "test_pics", "testpic_1.jpeg"))                 # Goes to the image and opens it
img = img.convert("RGB")                                                                # Converts it to RGB just in case if it is not
img = img.resize((10, 10))

channels = []                                         # Creates an empty array for the RGB channels of the pixels
modified = []                                         # Cretes and empty array for the modified bits
word_to_bit = ""                                      # Creates an empty string for the Binary of the words

def char_to_bin(a):                                   # Defining a Fucntion that returns the Binary of a Char
    return f"{ord(a):08b}"

def check_and_flip(binary_input,bit_input):           # Defininf a Fucntion that takes in a Binary and a Single Bit
    if binary_input[7] == bit_input:                  # and changes the LSB of the Binary to match the Single Bit
        return binary_input
    else:
        flipped_bit = "1" if binary_input[7] == "0" else "0"
        result = binary_input[:7] + flipped_bit
        return result

for i in range(0, img.width):                         # Gets the RGB Channels of each pixel and appends it to the Channels Array
    for j in range(0, img.height):
        r, g, b = img.getpixel((i, j))
        channels.append(r)
        channels.append(g)
        channels.append(b)


for i in word:                                       # Creates the Binary for the phrase/words using the Char_to_Bin Function
    if i == " ":
        continue
    else:
        word_to_bit = word_to_bit + char_to_bin(i)

for val,bit_input in zip(channels,word_to_bit):
    modified.append(check_and_flip(f"{val:08b}",bit_input))


print(channels, len(channels))
print(modified, len(modified))
print(word_to_bit, len(word_to_bit))


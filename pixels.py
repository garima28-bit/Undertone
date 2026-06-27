import os
from PIL import Image

base_dir = os.path.dirname(os.path.abspath(__file__))


img = Image.open(os.path.join(base_dir, "test_pics", "testpic_1.jpeg"))
img = img.convert("RGB")
img = img.resize((10, 10))


red = []
green = []
blue = []

for i in range(0, 10):
    for j in range(0, 10):
        r, g, b = img.getpixel((i, j))
        red.append(r)
        green.append(g)
        blue.append(b)

print(red, len(red))
print(green, len(green))
print(blue, len(blue))
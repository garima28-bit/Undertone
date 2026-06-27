from PIL import Image

img = Image.open("test_pics/testpic_1.jpeg")
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
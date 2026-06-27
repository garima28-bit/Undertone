import pixels

binary_red =[]
binary_blue = []
binary_green = []

def binary(number):
    binnum = f"{number:08b}"
    return binnum

for i in pixels.red:
    binary_red.append(binary(i))

for j in pixels.green:
    binary_green.append(binary(j))

for k in pixels.blue:
    binary_blue.append(binary(k))

print(binary_red, len(binary_red))
print(binary_green, len(binary_green))
print(binary_blue, len(binary_blue))
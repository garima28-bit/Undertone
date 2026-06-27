word = input("Please Enter your word: ")

def char_to_bin(a):
    return f"{ord(a):08b}"

for i in word:
    print(char_to_bin(i))
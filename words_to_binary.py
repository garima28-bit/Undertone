word = input("Please Enter your word: ")

def char_to_bin(a):
    return f"{ord(a):08b}"

for i in word:
    if i == " ":
        continue
    else:
        converted_val = char_to_bin(i)
        l_s_t = converted_val[7]
        print(converted_val, l_s_t)
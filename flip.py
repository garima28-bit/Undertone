binary_input = input("Enter 8 bit binary digit: ")
bit_input = input("Enter a single bit 0 or 1: ")

last_bit = binary_input[-1]

def check_and_flip(binary_input,bit_input):
    if last_bit == bit_input:
        return binary_input
    else:
        flipped_bit = "1" if last_bit == "0" else "0"
        result = binary_input[:7] + flipped_bit
        return result
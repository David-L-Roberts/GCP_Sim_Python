i = 244
num_bits = 9

binary_str = f"{i:0{num_bits}b}"  # Format the number as a binary string with leading zeros
print("Fist:\t", binary_str)

binary_str = binary_str[:5] + 'A' + binary_str[-3:]
print("Second:\t", binary_str)

binary_str = binary_str[:num_bits-5] + 'X' + binary_str[-5+1:]
print("Third:\t", binary_str)

# 0b011110100
# 0111XA100
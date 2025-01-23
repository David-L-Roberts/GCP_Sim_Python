# Function to format and print a binary number
def print_binary_strings(num_bits, count):
    for i in range(count):
        # Generate the binary representation of the number
        binary_str = f"{i:0{num_bits}b}"  # Format the number as a binary string with leading zeros

        # Convert the string into the desired format
        formatted_str = "{" + ", ".join(binary_str) + "}"

        # Print the formatted string
        print(f'{formatted_str},')
        print(binary_str)

        if (binary_str[-2] == '1') and (binary_str[-3] == '1'):
            print("Bazinga!")
        print()

# Parameters
num_bits = 9  # Number of binary digits
count = 10   # Number of binary strings to generate (2^9)

# Print the binary strings
print_binary_strings(num_bits, count)

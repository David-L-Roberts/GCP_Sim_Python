msg1 = b'<104>'
msg2 = b'<205>'

msg1_str = msg1.decode()
if (msg1_str[0] == '<'):
    print("TRUE")
else:
    print("FALSE")

print(msg2[1:-1])
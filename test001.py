# msg1 = b'Here is a message before code <104> I am after the code'
# msg1 = b'a <123> b <456> c <78>'
msg1 = b'just a text string'

msg1_str = msg1.decode()

msg1_split = msg1_str.split(sep="<")
print("Line 1: ", end="")
print(msg1_split)

msg1_split = [x.split(">") for x in msg1_split]
print("Line 2: ", end="")
print(msg1_split)

msg1_list = []
for subList in msg1_split:
    for element in subList:
        msg1_list.append(element)

print("Line 3: ", end="")
print(msg1_list)

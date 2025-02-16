# msg = b'Here is a message before code <104> I am after the code'
# msg = b'Here is a message before code <104> I am after the code <546> finale'
# msg = b'a <123> b <456> c <78>'
# msg = b'just a text string'
msg = b'a <123> b <456 c <78>'

msg_str = msg.decode()

msg_list = []
i = 0
j = 0   # prevent infinite loops
while True:
    j += 1
    if (i >= len(msg_str)) or (j > 250):
        break
        
    char = msg_str[i]
    if char == "<":
        msg_part1 = msg_str[:i]
        msg_part2 = msg_str[i:]

        msg_list.append(msg_part1)
        msg_str = msg_part2
        i = 1
        continue
    elif char == ">":
        i += 1
        msg_part1 = msg_str[:i]
        msg_part2 = msg_str[i:]

        msg_list.append(msg_part1)
        msg_str = msg_part2
        i=0
        continue

    i += 1

if msg_str != '':
    msg_list.append(msg_str)

print("Line 1: ", end="")
print(msg_list)
alphabet_list = ["A", "B", "C", "D", "E", "F", "G", "H", 
                 "I", "J", "K", "L", "M", "N", "O", "P", 
                 "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

alpha_ori_dic = {letter: i for i, letter in enumerate(alphabet_list)}

def encrypt_and_decrypt(key, msg):
    tmp_list = []
    for letter in msg:
        if letter not in alphabet_list:
            tmp_list.append(letter)
            continue
        tmp_list.append(alphabet_list[(alpha_ori_dic[letter]-key)%26])
    return "".join(tmp_list)

choice_in = None
while(choice_in not in ['d','e']):
    choice_in = input("Do you want to (e)ncrypt or (d)ecrypt?\n> ")

key = 1.5
while(key % int(key) > 0.0001):
    try:
        key = float(input("Please enter the key to use:\n> "))
    except (KeyError, ValueError):
        print("Please enter an integer")
    
    if key < 0.1:
        key = 0
        break

key = int(key)      
msg = input("Enter the message to encrypt:\n> ").upper()

if choice_in == 'e':
    final_msg = encrypt_and_decrypt(-key, msg)
elif choice_in == 'd':
    final_msg = encrypt_and_decrypt(key, msg)
    
print(final_msg)
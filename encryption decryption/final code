alph="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alph2="abcdefghijklmnopqrstuvwxyz"
newmessage=""
try:
    command=input("Do you want to (e)ncrypt or (d)ecrypt? enter e or d ")
    if command=='e':
        num=int(input("Please enter the key (0 to 25) to use? "))
        message=input("Enter the message? ")
        for i in range(len(message)):
            if message[i] not in alph and message[i] not in alph2:
                newmessage=newmessage+message[i]
            else:
                for j in range(len(alph)):
                    if message[i]==alph[j]:
                        a=j+num
                        if a<=26:
                            newmessage=newmessage+alph[a]
                        else:
                            newmessage=newmessage+alph[a-26]
                    elif message[i]==alph2[j]:
                        a=j+num
                        if a<=26:
                            newmessage=newmessage+alph2[a]
                        else:
                            newmessage=newmessage+alph2[a-26]
    if command=='d':
        num=int(input("Please enter the key (0 to 25) to use? "))
        message=input("Enter the message? ")
        for i in range(len(message)):
            if message[i] not in alph and message[i] not in alph2:
                newmessage=newmessage+message[i]
            else:
                for j in range(len(alph)):
                    if message[i]==alph[j]:
                        a=j-num
                        if a<=26:
                            newmessage=newmessage+alph[a]
                        else:
                            newmessage=newmessage+alph[a-26]
                    elif message[i]==alph2[j]:
                        a=j-num
                        if a<=26:
                            newmessage=newmessage+alph2[a]
                        else:
                            newmessage=newmessage+alph2[a-26]
    print(newmessage)
    if command!="e" and command!="d":
        print("Command should be e or d")
except:
    print("wrong input! ")

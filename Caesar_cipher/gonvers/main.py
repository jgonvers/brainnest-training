class CaesarCypher():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars_len = len(chars)
    def __init__(self, key=0):
        self.key = key
    def set_key(self, key):
        self.key = key
    def get_key(self):
        return self.key
    def encrypt(self, string):
        output = ""
        for char in string.upper():
            if char in self.chars:
                output += self.chars[(self.key+self.chars.index(char))%self.chars_len]
            else:
                output += char
        return output
    def decrypt(self, string):
        self.key *= -1
        output = self.encrypt(string)
        self.key *= -1
        return output
    

if __name__ == "__main__":
    cypher = CaesarCypher()
    while(True):
        match input("Do you want to : (e)ncrypt, (d)ecrypt, change the (k)ey or (q)uit\n").lower():
            case "q"|"quit":
                break
            case "e"|"encrypt":
                string = input("Give the string you want to encrypt\n")
                print(cypher.encrypt(string))
            case "d"|"decrypt":
                string = input("Give the string you want to decrypt\n")
                print(cypher.decrypt(string))
            case "k"|"key":
                key = input("give the new key\n")
                try:
                    key = int(key)
                except ValueError:
                    print(f"{key} is not a valid key")
                cypher.set_key(key)
            case _:
                print("not a valid command")
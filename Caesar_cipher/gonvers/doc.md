##CaesarCypher by gonvers joachim

```
class CaesarCypher:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars_len = len(chars)
```
create a class for the encrypt/decrypt
use a string (char list) instead of the ordinal value for the encrypt/decrypt because it allow to more easily handle the loop around with a modulo and the class can easily be extended to use a different order of chars
```
    def __init__(self, key=0):
        self.key = key
```
init the class with a key
```
    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key
```
setter and getter for the key
```
    def encrypt(self, string):
        output = ""
        for char in string.upper():
            if char in self.chars:
                output += self.chars[
                    (self.key + self.chars.index(char)) % self.chars_len
                ]
            else:
                output += char
        return output
```
encrypt
for each char in the string find the corresponding index in the reference string add to it the key and use modulo to loop around
if the char is not in the reference do not change it
```
    def decrypt(self, string):
        self.key *= -1
        output = self.encrypt(string)
        self.key *= -1
        return output
```
decrypt by encrypting by the negative of the key
the modification of the key to do that make it not safe to use in parallele with itself
```
if __name__ == "__main__":
    cypher = CaesarCypher()
    while True:
        match input(
            "Do you want to : (e)ncrypt, (d)ecrypt, change the (k)ey or (q)uit\n"
        ).lower():
            case "q" | "quit":
                break
            case "e" | "encrypt":
                string = input("Give the string you want to encrypt\n")
                print(cypher.encrypt(string))
            case "d" | "decrypt":
                string = input("Give the string you want to decrypt\n")
                print(cypher.decrypt(string))
            case "k" | "key":
                key = input("give the new key\n")
                try:
                    key = int(key)
                except ValueError:
                    print(f"{key} is not a valid key")
                cypher.set_key(key)
            case _:
                print("not a valid command")
```
GUI using the console and a switch for the options
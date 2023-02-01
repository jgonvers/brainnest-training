def encrypt(key=0,phrase=""):
    encrypted_phrase = ""
    key = key % 26
    for letter in phrase:
        if letter.isalpha():
            ascii_position = ord(letter) + key
            if ascii_position > 90:
                ascii_position = 65 + (ascii_position - 91)
            encrypted_phrase += chr(ascii_position)
        else:
            encrypted_phrase += letter
    return encrypted_phrase


def decrypt(key=0, phrase=""):
    decrypted_phrase = ""
    key %= 26
    for letter in phrase:
        if letter.isalpha():
            ascii_position = ord(letter) - key
            if ascii_position < 65:
                ascii_position = 91 - (65 - ascii_position)
            decrypted_phrase += chr(ascii_position)
        else:
            decrypted_phrase += letter
    return decrypted_phrase


def main():
    while True:
        inp = input("Do you want to (e)ncrypt or (d)ecrypt? (x to quit)\n")
        if inp == 'x':
            print("Exiting...")
            break
        
        if inp not in ['e', 'd']:
            print("Invalid option.")
            continue

        try:
            key = int(input("Please enter the key (0 to 25) to use.\n"))
            if key < 0 or key > 25:
                raise ValueError("Key must be between 0 and 25.")
        except ValueError as e:
            print(f"Invalid key: {e}")
            continue

        phrase = input("Enter the message to {}.".format("encrypt" if inp == 'e' else "decrypt"))
        if inp == 'e':
            print(encrypt(key, phrase))
        else:
            print(decrypt(key, phrase))

if __name__ == "__main__":
    main()
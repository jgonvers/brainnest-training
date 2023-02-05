"""Caesar cipher implementation."""


class CaesarCipher:
    def __init__(self):
        self.dictionary_size = 26
        self.valid_commands = ["e", "d", "exit"]
        self.encrypt = True
        self.cipher_valid_shift = range(self.dictionary_size)

    def encrypt_text(self, text: str, shift: int) -> str:
        return "".join(self._transform_character(shift, char) for char in text)

    def decrypt_text(self, text: str, shift: int) -> str:
        self.encrypt = False
        return "".join(self._transform_character(shift, char) for char in text)

    def _handle_out_of_bound_case(self, ord_char: int, bound: int) -> str:
        if ord_char > bound and self.encrypt:  # out of bound case
            return ord_char - self.dictionary_size
        elif ord_char < bound and not self.encrypt:  # out of bound case
            return ord_char + self.dictionary_size
        return ord_char

    def _transform_character(self, shift: int, char: str) -> str:
        if not char.isalpha():  # just return not character
            return char
        bound = ord("z")  # bound for encryption
        if not self.encrypt:
            shift = -shift
            bound = ord("a")  # bound for decryption
        char_case = char.isupper()  # remember case of character
        new_char = ord(char.lower()) + shift
        new_char = self._handle_out_of_bound_case(
            ord_char=new_char, bound=bound
        )
        return chr(new_char).upper() if char_case else chr(new_char)


if __name__ == "__main__":
    command = ""
    shift = -1
    cipher = CaesarCipher()
    try:
        while command not in cipher.valid_commands:
            command = input(
                "Do you want to (e)ncrypt or (d)ecrypt?\n"
                "Or write 'exit' to finish\n"
            )
            if command not in cipher.valid_commands:
                print("INVALID COMMAND!")
            elif command == "exit":
                exit()
        while shift not in cipher.cipher_valid_shift:
            shift = int(input("Please enter the key (0 to 25) to use.\n"))
            if shift not in cipher.cipher_valid_shift:
                print("INVALID KEY!")
        text = input("Enter your message:\n")
        if command == "e":
            print(cipher.encrypt_text(text, shift))
        else:
            print(cipher.decrypt_text(text, shift))
    except Exception as e:
        print(f"Something went wrong. {e}")

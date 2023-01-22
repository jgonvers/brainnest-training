import tkinter as tk


class TKUtils:
    @staticmethod
    def create_button(
        window, text, command, width=24, font=24, bg="white", fg="black", bd=2
    ):
        return tk.Button(
            window,
            text=text,
            width=width,
            font=font,
            bg=bg,
            fg=fg,
            bd=bd,
            command=command,
        )

    @staticmethod
    def create_label(window, text, width=24, bg="white", fg="black", font=4):
        return tk.Label(
            window,
            text=text,
            width=width,
            bg=bg,
            fg=fg,
            font=font,
        )

    @staticmethod
    def create_entry(window, width=10, bg="white", fg="black", font=4):
        return tk.Entry(
            window,
            width=width,
            bg=bg,
            fg=fg,
            font=font,
        )

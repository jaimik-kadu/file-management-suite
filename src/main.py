import sv_ttk
from tkinter import ttk
import tkinter as tk

from menu import Menu
from content import Content


class FileManagementSuite(tk.Tk):
    def __init__(self):
        super().__init__()
        sv_ttk.set_theme("dark")
        self.title("File Management Suite")
        self.geometry("1000x600")
        self.minsize(1000,600)

        # Configure grid layout for the root window
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=8)
        self.grid_rowconfigure(3, weight=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=5)
        self.grid_columnconfigure(3, weight=1)

        lbl_title = ttk.Label(self, text="Dashboard", font=("Helvetica", 20, "bold"), width=15)
        lbl_title.grid(row=0, column=1, sticky="sw")

        self.content = Content(self)
        self.content.grid(row=2, column=2, sticky="nswe")  # Attach Content frame

        self.menu = Menu(self)
        self.menu.grid(row=2, column=1, sticky="nswe")  # Attach Menu frame

        self.mainloop()

if __name__ == "__main__":
    app = FileManagementSuite()
    app.mainloop()
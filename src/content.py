from tkinter import ttk

class Content(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, sticky="nswe")

        # Define a style for the buttons
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Helvetica", 16))

        self.create_widgets()
    
    def create_widgets(self):
        placeholder = ttk.Label(self, text=" Select a feature from the sidebar to get started.", font=("Helvetica", 14))
        placeholder.grid(row=0, column=0, sticky='nswe', pady=(10, 20))
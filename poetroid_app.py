import tkinter as tk
from main_screen import MainScreen

class PoetroidApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('480x800')
        self.main_screen = MainScreen(self)
        self.attributes('-fullscreen', True)


if __name__ == '__main__':
    app = PoetroidApp()
    app.mainloop()

import tkinter as tk
from main_screen import MainScreen
import subprocess
import time


class PoetroidApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('480x800')
        self.main_screen = MainScreen(self)
        self.attributes('-fullscreen', True)
        self.check_network_connection()

    def check_network_connection(self):
        def ping():
            try:
                subprocess.check_call(['ping', '-c', '1', '8.8.8.8'],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
                self.main_screen.update_ui()
                return True
            except subprocess.CalledProcessError:
                self.after(30000, check_connection)
                return False

        def check_connection():
            if not ping():
                self.main_screen.show_network_error()

        check_connection()


if __name__ == '__main__':
    app = PoetroidApp()
    app.mainloop()

import tkinter as tk
from main_screen import MainScreen
import subprocess
import threading
import time

class PoetroidApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('480x800')
        self.network_alert = None
        self.check_network()  # Start network checking before creating main screen
        self.main_screen = MainScreen(self)

    def check_network(self):
        def ping():
            try:
                subprocess.check_call(
                    ['ping', '-c', '1', '8.8.8.8'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return True
            except subprocess.CalledProcessError:
                return False

        def show_network_alert():
            if self.network_alert is None:
                self.network_alert = tk.Toplevel(self)
                self.network_alert.geometry('400x200')
                self.network_alert.title('Network Error')
                self.network_alert.transient(self)
                self.network_alert.protocol('WM_DELETE_WINDOW', lambda: None)  # Prevent closing
                
                msg = tk.Label(
                    self.network_alert,
                    text='No internet connection detected.\nPlease connect to WiFi.',
                    font=('Arial', 14),
                    wraplength=350
                )
                msg.pack(expand=True)

        def hide_network_alert():
            if self.network_alert is not None:
                self.network_alert.destroy()
                self.network_alert = None

        def check_connection():
            if ping():
                hide_network_alert()
            else:
                show_network_alert()
            # Schedule next check in 3 seconds
            self.after(3000, check_connection)

        # Start the initial check
        check_connection()

if __name__ == '__main__':
    app = PoetroidApp()
    app.mainloop()
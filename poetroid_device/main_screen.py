import tkinter as tk
from PIL import Image, ImageTk
import os
import yaml
from capture_screen import CaptureScreen
import subprocess


class MainScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure_layout()

        self.current_category_index = 0
        self.current_item_index = 0
        self.focus_on_category = False
        self.printing_enabled = True
        self.capture_initiated = False

        self.load_configuration()
        self.update_ui()  # Call update_ui to ensure UI is correctly initialized

        # Bind keyboard events
        self.master.bind('<t>', self.toggle_focus_event)
        self.master.bind('<p>', self.toggle_printing_event)
        self.master.bind('<j>', lambda event: self.navigate_items(-1))
        self.master.bind('<l>', lambda event: self.navigate_items(1))
        self.master.bind('<s>', self.shutter_key_down)
        self.master.bind('m', self.reset_app_event)  # Bind 'm' as a reset key

        self.check_network_connection()

    def configure_layout(self):
        self.master.title('POETROID')
        self.pack(fill=tk.BOTH, expand=True)

        self.title_bar = tk.Label(self, text='POETROID', font=('Arial', 24))
        self.title_bar.pack(side=tk.TOP, fill=tk.X)

        self.category_panel = tk.Frame(self, borderwidth=5, relief='solid')
        self.category_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.category_emoji = tk.Label(
            self.category_panel, font=('Arial', 100))
        self.category_emoji.pack()

        self.item_panel = tk.Frame(self, borderwidth=5, relief='solid')
        self.item_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.item_image_label = tk.Label(self.item_panel)
        self.item_image_label.pack()

        self.controls_panel = tk.Frame(self)
        self.controls_panel.pack(side=tk.BOTTOM, fill=tk.X)

        self.printer_icon = tk.Label(
            self.controls_panel, text='Print', font=('Arial', 16))
        self.printer_icon.pack(side=tk.LEFT)

    def load_configuration(self):
        with open('./categories.yaml', 'r') as file:
            self.categories = yaml.safe_load(file)['categories']
        with open('./models.yaml', 'r') as file:
            self.models = yaml.safe_load(file)['models']

    def update_ui(self):
        self.configure_layout()  # Reconfigure the layout to update border colors dynamically
        emoji_name = self.categories[self.current_category_index]['emoji']
        self.category_emoji['text'] = emoji_name

        item = self.categories[self.current_category_index]['prompts'][self.current_item_index]
        img_path = os.path.join('./imgs', item['imagefilename'])
        self.update_image(img_path)

        self.printer_icon['text'] = 'Print Enabled' if self.printing_enabled else 'Print Disabled'

    def update_image(self, img_path):
        img = Image.open(img_path)
        photo = ImageTk.PhotoImage(img)
        self.item_image_label.photo = photo  # Keep a reference
        self.item_image_label.config(image=photo)
        self.item_image_label.pack_forget()
        self.item_image_label.pack(
            side=tk.TOP, anchor=tk.CENTER, fill=tk.BOTH, expand=True)

    def toggle_focus(self):
        self.focus_on_category = not self.focus_on_category
        self.update_ui()

    def toggle_category(self, direction):
        num_categories = len(self.categories)
        self.current_category_index = (
            self.current_category_index + direction) % num_categories
        self.current_item_index = 0
        self.update_ui()

    def toggle_item(self, direction):
        num_items = len(
            self.categories[self.current_category_index]['prompts'])
        self.current_item_index = (
            self.current_item_index + direction) % num_items
        self.update_ui()

    def toggle_printing(self):
        self.printing_enabled = not self.printing_enabled
        self.update_ui()

    def toggle_focus_event(self, event):
        self.toggle_focus()

    def toggle_printing_event(self, event):
        self.toggle_printing()

    def navigate_items(self, direction):
        if self.focus_on_category:
            self.toggle_category(direction)
        else:
            self.toggle_item(direction)

    def reset_app(self):
        self.current_category_index = 0
        self.current_item_index = 0
        self.focus_on_category = False
        self.capture_initiated = False
        if hasattr(self, 'capture_screen'):
            self.capture_screen.destroy()
            delattr(self, 'capture_screen')
        self.update_ui()

    def reset_app_event(self, event):
        self.reset_app()

    def shutter_key_down(self, event):
        if not self.capture_initiated:
            self.capture_initiated = True
            self.capture_screen = CaptureScreen(self.master, self)
            self.master.after(0, self.capture_screen.capture_and_process_image)
        else:
            print("Capture is already initiated or capture_screen still exists.")

    def check_network_connection(self):
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

        def check_connection():
            if not ping():
                self.show_network_error()
                self.master.after(30000, check_connection)

        check_connection()

    def show_network_error(self):
        error_window = tk.Toplevel(self)
        error_window.geometry('300x100')
        error_window.title('Network Error')
        tk.Label(error_window,
                 text='Network error. Please check your connection.').pack()
        tk.Button(error_window, text='OK', command=lambda: [
                  error_window.destroy(), self.check_network_connection()]).pack()

    def display_network_error(self):
        error_label = tk.Label(
            self, text="Network Error: Please check your internet connection.", fg="red")
        error_label.pack(pady=10)
        self.update_ui()
        # Destroy error message after 30 seconds
        error_label.after(30000, error_label.destroy)

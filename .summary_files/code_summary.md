Output of tree command:
```
|-- LICENSE
|-- README.md
|-- __pycache__
|-- poetroid_device
    |-- __pycache__
    |-- capture_screen.py
    |-- categories.yaml
    |-- imgs
        |-- adventure_landscape.jpg
        |-- alien.jpg
        |-- backstory.jpg
        |-- biology.jpg
        |-- bukowski.jpg
        |-- compliment.jpg
        |-- conspiracy_theory.jpg
        |-- coronation.jpg
        |-- cthulhu.jpg
        |-- cthulu.jpg
        |-- cult.jpg
        |-- daring_escape.jpg
        |-- dickinson.jpg
        |-- discovery.jpg
        |-- environment.jpg
        |-- epic_battle.jpg
        |-- epicurus.jpg
        |-- expression_of_love.jpg
        |-- extreme_sport.jpg
        |-- frost.jpg
        |-- future.jpg
        |-- ghost.jpg
        |-- ghost_story.jpg
        |-- ginsberg.jpg
        |-- haiku.jpg
        |-- horror_movie.jpg
        |-- ideal_date.jpg
        |-- keats.jpg
        |-- kerouac.jpg
        |-- legendary_creature.jpg
        |-- lost_love.jpg
        |-- love_letter.jpg
        |-- mad_scientist.jpg
        |-- magic_spell.jpg
        |-- monster.jpg
        |-- mythical_realm.jpg
        |-- nightmare.jpg
        |-- observational.jpg
        |-- outside.jpg
        |-- overanalyze.jpg
        |-- philosophy.jpg
        |-- physics.jpg
        |-- plato.jpg
        |-- poe.jpg
        |-- poetroid.jpg
        |-- queneau.jpg
        |-- ritual.jpg
        |-- roast.jpg
        |-- rumi.jpg
        |-- satire.jpg
        |-- scary_story.jpg
        |-- science_scene.jpg
        |-- serendipity.jpg
        |-- seuss.jpg
        |-- shakespeare.jpg
        |-- silverstein.jpg
        |-- slapstick.jpg
        |-- technology.jpg
        |-- test.jpg
        |-- treasure_hunt.jpg
        |-- whitman.jpg
        |-- wilde.jpg
    |-- main_screen.py
    |-- models.yaml
    |-- poetroid.png
    |-- poetroid_app.py
    |-- poetroid_device.png
    |-- requirements.txt
    |-- seguiemj.ttf
    |-- start.sh
    |-- uploads
        |-- 0904cd63-d242-4660-9077-1e014a01d0f5.jpg
        |-- 1cee5c11-4626-4de0-984e-f65b5f586af6.jpg
        |-- 1d4f9951-eef9-480f-985c-d8b4de28acf3.jpg
        |-- 23700d72-d399-4984-b40c-47fe70d39c37.jpg
        |-- 45a7d858-369c-476b-8d87-a93cfe841511.jpg
        |-- 60526da7-7d71-4c2b-98b6-048d96131251.jpg
        |-- 63479b7c-548d-47da-8879-33144b49d776.jpg
        |-- 6a009377-d044-4729-a3d6-8cbc5c58bec4.jpg
        |-- 7644caa2-48fd-46b6-930c-e49cc05d8b17.jpg
        |-- 7c07048c-6feb-4ad0-8838-18eae06fef55.jpg
        |-- 80403722-9b10-4160-91b0-0083ce46ce34.jpg
        |-- 894e679d-2e88-47c1-aeb7-04775daa661b.jpg
        |-- 9d8c85f3-c6a0-4bd7-920f-8b5e4ece9f26.jpg
        |-- a3a14d3b-c065-414d-bedd-21a1c5a50baf.jpg
        |-- a7862da4-222c-4ee9-a2cc-ba211b1b9de0.jpg
        |-- a81d538c-59e9-41de-aec8-df5bfc755c09.jpg
        |-- a9c620ca-bfdc-44d4-9e9c-979ddecda8ba.jpg
        |-- af1ebe3a-dbaa-487a-904f-9e7a2f126db7.jpg
        |-- bc968638-c664-40d1-9314-615b5c3af7e4.jpg
        |-- c295593d-9dc4-45c2-aead-8cfc0723f857.jpg
        |-- c9070692-3cc0-4819-b32a-cfea63fcf6c2.jpg
        |-- d4029a25-d0a4-47a4-913c-4e309b5594f8.jpg
        |-- d84d59b8-c692-48f3-a082-cee166f02cb8.jpg
        |-- e6e0b0f4-5a7f-4fdd-aec2-ef25e4e1241a.jpg
        |-- f56f7937-1eb8-4895-8d3c-bdf6ad10669c.jpg
        |-- faea9aab-0b87-4c7e-bd31-a80e9179ca67.jpg
|-- tools
    |-- add_imgs.py

```

---

./poetroid_device/poetroid_app.py
```
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
```
---

./poetroid_device/capture_screen.py
```
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import base64
import requests
import time
import uuid
import os
import logging
# import sys


class CaptureScreen(tk.Toplevel):
    def __init__(self, master, main_screen):
        super().__init__(master)
        self.geometry('480x800')
        self.main_screen = main_screen
        self.status_label = tk.Label(
            self, text='Thinking...', font=('Arial', 48), wraplength=480)
        self.status_label.pack()
        self.capture_and_process_image()

    def capture_and_process_image(self):
        # Update the status label immediately
        self.status_label['text'] = 'Thinking...'
        self.update()  
        camera_index = 0  
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            camera_index = 1
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                self.status_label['text'] = 'Error: Could not open camera.'
                return

        warm_up_time = 2  # Warm-up time in seconds
        start_time = time.time()

        # Warm-up phase: Capture and discard frames for the warm-up period
        print("Warming up the camera...")
        self.status_label['text'] = 'Warming up the camera...'
        while time.time() - start_time < warm_up_time:
            ret, frame = cap.read()
            if not ret:
                self.status_label['text'] = "Error: Could not read frame from the camera during warm-up."
                cap.release()
                return
        self.status_label['text'] = 'Ready to capture.'
        _, buffer = cv2.imencode('.jpg', frame)
        self.status_label['text'] = 'Capturing...'
        binary_image = buffer.tobytes()
        self.status_label['text'] = 'Processing...'
        print('\a')

        # Generate a safe UUID for the filename
        unique_filename = str(uuid.uuid4()) + '.jpg'
        uploads_dir = './uploads'
        if not os.path.exists(uploads_dir):
            # Create the uploads directory if it doesn't exist
            os.makedirs(uploads_dir)

        file_path = os.path.join(uploads_dir, unique_filename)
        # Account for upside down camera.
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        # Save the image to the ./uploads directory with the UUID filename
        with open(file_path, 'wb') as f:
            f.write(binary_image)

        main_screen = self.main_screen

        category_index = self.main_screen.current_category_index
        item_index = self.main_screen.current_item_index
        prompt = self.main_screen.categories[category_index]['prompts'][item_index]['prompt']
        # get the file as a binary string
        with open(file_path, 'rb') as f:
            file_data = f.read()
        # encode the binary string as base64
        base64_data = base64.b64encode(file_data)
        # decode the base64 string into utf-8
        base64_string = base64_data.decode('utf-8')
        # print("Sending request with prompt: " + prompt)
        try:
            response = requests.post(
                "https://roast.wayr.app/behold",
                data={
                    "prompt": "Describe this image in as much detail as possible. Be as verbose as possible. List every item you see and describe it verbosely.",
                    "file": base64_string
                },
                # Open and send the image file
                files={'file': open(file_path, 'rb')},
                timeout=60
            )
            response.raise_for_status()
            response_data = response.json()
            print("Image description:" + response_data['response'])
        except requests.RequestException as e:
            self.status_label['text'] = 'Failed to get response.'
            print(e)

        # addthe response to the prompt
        # prompt = prompt + "Here is the image description:" + response_data['response']
        print("Sending request with prompt: " + prompt)
        prompt = prompt + " Keep it short and sweet. Do not directly refer to the subject in this prompt." + \
            "Here is the image description" + response_data['response']
        try:
            response = requests.post(
                # make prompt url safe
                "https://roast.wayr.app/infer/?prompt=" + prompt,
            )
            response.raise_for_status()
            response_data = response.json()
            print("Final result: " + response_data['response'])
            self.display_response(response_data['response'])
        except requests.RequestException as e:
            self.status_label['text'] = 'Failed to get response.'
            print(e)

        # Close the video capture
        cap.release()

    def display_response(self, response_text):
        # self.status_label['text'] = response_text
        self.status_label['wraplength'] = 480  # Wrap the result
        # Handle printing
        if self.main_screen.printing_enabled:
            try:
                with open('/dev/usb/lp0', 'w') as printer:
                    printer.write(response_text + '\n\n\n\n\n')
            except IOError as e:
                logging.error(f'Print: Failed to print to /dev/usb/lp0: {e}')
                self.status_label['text'] = 'Failed to print.'
        self.reset_to_main()

    def reset_to_main(self):
        # self.master.mainloop()  # Restart the tkinter mainloop before destroy
        self.capture_initiated = False
        self.destroy()  # Close the capture screen and reset
        self.main_screen.update_ui()

    def display_test_image(self, image_path):
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(self, image=photo)
        label.image = photo  # Keep a reference.
        label.pack()
        self.show_reset_button()

    def show_reset_button(self):
        reset_button = tk.Button(
            self, text='Reset', command=self.reset_to_main)
        reset_button.pack()
```
---

./poetroid_device/main_screen.py
```
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
```
---

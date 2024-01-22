import tkinter as tk
from PIL import Image, ImageTk
import os
import yaml
import threading
import cv2
import base64
import requests
import time
import base64
import logging
import uuid

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
        # get s down and release events and start the capture screen
        self.master.bind('<s>', self.shutter_key_down)


    def configure_layout(self):
        self.master.title('POETROID')
        self.pack(fill=tk.BOTH, expand=True)

        self.title_bar = tk.Label(self, text='POETROID', font=('Arial', 24))
        self.title_bar.pack(side=tk.TOP, fill=tk.X)

        self.category_panel = tk.Frame(self, borderwidth=2, relief='solid')
        self.category_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.category_emoji = tk.Label(self.category_panel, font=('Arial', 100))
        self.category_emoji.pack()

        self.item_panel = tk.Frame(self, borderwidth=2, relief='solid')
        self.item_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.item_image_label = tk.Label(self.item_panel)
        self.item_image_label.pack()

        self.controls_panel = tk.Frame(self)
        self.controls_panel.pack(side=tk.BOTTOM, fill=tk.X)

        self.printer_icon = tk.Label(self.controls_panel, text='Print', font=('Arial', 16))
        self.printer_icon.pack(side=tk.LEFT)

    def load_configuration(self):
        with open('./categories.yaml', 'r') as file:
            self.categories = yaml.safe_load(file)['categories']
        with open('./models.yaml', 'r') as file:
            self.models = yaml.safe_load(file)['models']

    def update_ui(self):
        emoji_name = self.categories[self.current_category_index]['emoji']
        self.category_emoji['text'] = emoji_name

        item = self.categories[self.current_category_index]['prompts'][self.current_item_index]
        img_path = os.path.join('./imgs', item['imagefilename'])
        self.update_image(img_path)
        self.printer_icon['text'] = 'Print Enabled' if self.printing_enabled else 'Print Disabled'

    def update_image(self, img_path):
        img = Image.open(img_path)
        photo = ImageTk.PhotoImage(img)
        self.item_image_label.photo = photo  # Keep a reference to avoid garbage collection
        self.item_image_label.config(image=photo)

    def toggle_focus(self):
        self.focus_on_category = not self.focus_on_category

    def toggle_category(self, direction):
        num_categories = len(self.categories)
        self.current_category_index = (self.current_category_index + direction) % num_categories
        self.current_item_index = 0
        self.update_ui()

    def toggle_item(self, direction):
        num_items = len(self.categories[self.current_category_index]['prompts'])
        self.current_item_index = (self.current_item_index + direction) % num_items
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
    
    def shutter_key_down(self, event):
        if not self.capture_initiated and not hasattr(self, 'capture_screen'):
            self.capture_initiated = True
            self.capture_screen = CaptureScreen(self.master, self)
            self.master.after(0, self.capture_screen.capture_and_process_image)
        else:
            print("Capture is already initiated or capture_screen still exists.")


    
class CaptureScreen(tk.Toplevel):
    def __init__(self, master, main_screen):
        super().__init__(master)
        self.geometry('480x800')  # Set the size
        self.main_screen = main_screen  # Reference to MainScreen
        self.status_label = tk.Label(self, text='Thinking...', font=(
            'Arial', 24), wraplength=480)  # Larger font and wrap context
        self.status_label.pack()

    # def start_processing(self):
    #     camera_index = 0  # Replace with the correct camera index from your tests
    #     cap = cv2.VideoCapture(camera_index)
    #     if not cap.isOpened():
    #         # Load a test image if no camera is found
    #         self.display_test_image('./poetroid.png')
    #         return
   
    def capture_and_process_image(self):
        camera_index = 1  # Replace with the correct camera index from your tests
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            self.status_label['text'] = f"Error: Could not open camera at index {camera_index}."
            return

        warm_up_time = 2  # Warm-up time in seconds
        start_time = time.time()

        # Warm-up phase: Capture and discard frames for the warm-up period
        print("Warming up the camera...")
        while time.time() - start_time < warm_up_time:
            ret, frame = cap.read()
            if not ret:
                self.status_label['text'] = "Error: Could not read frame from the camera during warm-up."
                cap.release()
                return

        _, buffer = cv2.imencode('.jpg', frame)
        binary_image = buffer.tobytes()

        # Generate a safe UUID for the filename
        unique_filename = str(uuid.uuid4()) + '.jpg'
        uploads_dir = './uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)  # Create the uploads directory if it doesn't exist
        
        file_path = os.path.join(uploads_dir, unique_filename)

        # Save the image to the ./uploads directory with the UUID filename
        with open(file_path, 'wb') as f:
            f.write(binary_image)

        main_screen = self.main_screen

        category_index = self.main_screen.current_category_index
        item_index = self.main_screen.current_item_index
        prompt = self.main_screen.categories[category_index]['prompts'][item_index]['prompt']
        #get the file as a binary string
        with open(file_path, 'rb') as f:
            file_data = f.read()
        #encode the binary string as base64
        base64_data = base64.b64encode(file_data)
        #decode the base64 string into utf-8
        base64_string = base64_data.decode('utf-8')
        # print("Sending request with prompt: " + prompt)
        try:
            response = requests.post(
                "https://roast.wayr.app/behold/",  
                data={
                    "prompt": "Describe this image in as much detail as possible. Be as verbose as possible. List every item you see and describe it verbosely.",
                    "file": base64_string
                },
                files={'file': open(file_path, 'rb')},  # Open and send the image file
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
        print ("Sending request with prompt: " + prompt)
        prompt = prompt + " Keep it short and sweet." + "Here is the image description" + response_data['response']
        try:
            response = requests.post(
                #make prompt url safe
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
        self.status_label['text'] = response_text
        self.status_label['wraplength'] = 480  # Wrap the result
        # Handle printing
        if self.main_screen.printing_enabled:
            try:
                with open('/dev/usb/lp0', 'w') as printer:
                    printer.write(response_text + '\n\n\n\n\n')
            except IOError as e:
                logging.error(f'Print: Failed to print to /dev/usb/lp0: {e}')
                self.status_label['text'] = 'Failed to print.'
        go_back_button = tk.Button(
            self, text='Go back', command=self.reset_to_main)
        go_back_button.pack()

    def reset_to_main(self):
        self.master.mainloop()  # Restart the tkinter mainloop before destroy
        self.destroy()  # Close the capture screen
        self.main_screen.master.deiconify()  # Show the main screen
        self.main_screen.update_ui()


    def display_test_image(self, image_path):
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(self, image=photo)
        label.image = photo  # Keep a reference.
        label.pack()
        self.show_reset_button()

    def show_reset_button(self):
        reset_button = tk.Button(self, text='Reset', command=self.reset_to_main)
        reset_button.pack()



class PoetroidApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('480x800')
        self.main_screen = MainScreen(self)
        self.attributes('-fullscreen', True)   
             

if __name__ == '__main__':
    app = PoetroidApp()
    app.mainloop()
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import base64
import requests
import time
import uuid
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERVER_BASEURL = os.getenv('SERVER_BASEURL', 'http://localhost:3090')
# In capture_screen.py, add near the top:
CAMERA_ROTATE = os.getenv('CAMERA_ROTATE', 'false').lower() == 'true'

class CaptureScreen(tk.Toplevel):
    def __init__(self, master, main_screen):
        super().__init__(master)
        self.geometry('480x800')
        self.main_screen = main_screen
        self.status_label = tk.Label(
            self, text='Thinking...', font=('Arial', 48), wraplength=480)
        self.status_label.pack()
        self.capture_and_process_image()

    def auto_reset(self):
        self.main_screen.capture_initiated = False
        self.destroy()
        self.main_screen.update_ui()

    def capture_and_process_image(self):
        # self.status_label['text'] = 'Warming Up...'
        # self.update()  
        camera_index = 0  
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            camera_index = 1
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                self.status_label['text'] = 'Error: Could not open camera.'
                return

        warm_up_time = 2
        start_time = time.time()
        # self.status_label['text'] = 'Warming up the camera...'
        while time.time() - start_time < warm_up_time:
            ret, frame = cap.read()
            if not ret:
                self.status_label['text'] = "Error: Could not read frame from the camera during warm-up."
                cap.release()
                return
        self.status_label['text'] = 'Processing...'
        self.update()  
        if CAMERA_ROTATE:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        _, buffer = cv2.imencode('.jpg', frame)
        binary_image = buffer.tobytes() 
        print('\a')
        cap.release()

        unique_filename = str(uuid.uuid4()) + '.jpg'
        uploads_dir = './uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        file_path = os.path.join(uploads_dir, unique_filename)
        with open(file_path, 'wb') as f:
            f.write(binary_image)

        category_index = self.main_screen.current_category_index
        item_index = self.main_screen.current_item_index
        prompt = self.main_screen.categories[category_index]['prompts'][item_index]['prompt']
        prompt = "You are poetroid, a poetry printing instant camera. " + prompt + " Be sure to include elements unique to the person, people, or subject in the image. Keep it short and sweet. Your response should only contain the requested poem and nothing else."

        try:
            response = requests.post(
                f"{SERVER_BASEURL}/generate_poem",
                data={"prompt": prompt},
                files={"file": open(file_path, 'rb')},
                timeout=60
            )
            response.raise_for_status()
            response_data = response.json()
            print("Generated poem: " + response_data['response'])
            self.display_response(response_data['response'])
        except requests.RequestException as e:
            self.status_label['text'] = 'Failed to get response.'
            print(e)
            # Schedule auto-reset after 3 seconds
            self.after(3000, self.auto_reset)

    def display_response(self, response_text):
        self.status_label['wraplength'] = 480
        # append two new lines and "-Poetroid" at the end of response_text
        response_text = response_text + '\n\n\n-Poetroid-\n\n'
        if self.main_screen.printing_enabled:
            try:
                with open('/dev/usb/lp0', 'w') as printer:
                    printer.write(response_text + '\n\n\n\n\n')
            except IOError as e:
                logging.error(f'Print: Failed to print to /dev/usb/lp0: {e}')
                self.status_label['text'] = 'Failed to print.'
        self.reset_to_main()

    def reset_to_main(self):
        self.main_screen.capture_initiated = False
        self.destroy()
        self.main_screen.update_ui()
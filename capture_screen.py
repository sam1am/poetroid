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
                "https://roast.wayr.app/behold/",
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

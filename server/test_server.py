#!/usr/bin/env python3
"""
Test script for the Poetroid server
Selects a random image from uploads folder and sends it to the server
"""
import os
import random
import requests
import time

# Configuration
SERVER_URL = "http://localhost:3090/generate_poem"
UPLOADS_DIR = "./uploads"
TEST_PROMPT = "write a short haiku poem"

def main():
    # Get all image files from uploads directory
    if not os.path.exists(UPLOADS_DIR):
        print(f"Error: {UPLOADS_DIR} directory not found!")
        return

    image_files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print(f"Error: No images found in {UPLOADS_DIR}")
        return

    # Select a random image
    selected_image = random.choice(image_files)
    image_path = os.path.join(UPLOADS_DIR, selected_image)

    print(f"Testing Poetroid server at {SERVER_URL}")
    print(f"Selected image: {selected_image}")
    print(f"Prompt: {TEST_PROMPT}")
    print("-" * 60)

    # Prepare the request
    try:
        with open(image_path, 'rb') as img_file:
            files = {
                'file': (selected_image, img_file, 'image/jpeg')
            }
            data = {
                'prompt': TEST_PROMPT
            }

            print("\nSending request to server...")
            start_time = time.time()
            response = requests.post(SERVER_URL, files=files, data=data, timeout=120)
            elapsed_time = time.time() - start_time

            print(f"Request completed in {elapsed_time:.2f} seconds")

            if response.status_code == 200:
                result = response.json()
                if 'response' in result:
                    print("\n✓ Success! Generated poem:")
                    print("=" * 60)
                    print(result['response'])
                    print("=" * 60)
                elif 'error' in result:
                    print(f"\n✗ Server returned error: {result['error']}")
            else:
                print(f"\n✗ Request failed with status code: {response.status_code}")
                print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to server. Is it running?")
    except requests.exceptions.Timeout:
        print("\n✗ Error: Request timed out (>120s)")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == "__main__":
    main()

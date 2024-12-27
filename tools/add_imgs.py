import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
import requests
from PIL import Image

# Load environment variables from a .env file located in the same directory as this script
load_dotenv()

client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

# Helper function to load contents from a YAML file
def load_yaml_file(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

# Check if image exists locally
def image_exists(imagefilename, img_directory='./imgs'):
    return os.path.isfile(os.path.join(img_directory, imagefilename))

# Generate image using OpenAI's DALL-E 3 API
def generate_image(prompt_text, imagefilename, img_directory='./imgs'):
    try:
        headers = {
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'prompt': prompt_text,
            'n': 1,
            'size': '1024x1024',
            'model': 'dall-e-3',
            'response_format': 'url',
        }
        
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers=headers,
            json=data
        )
        
        response.raise_for_status()
        images = response.json()['data']
        image_url = images[0]['url']
        
        # Download the image
        download_image(image_url, os.path.join(img_directory, imagefilename))
        
        # Resize the image to 300x300
        im = Image.open(os.path.join(img_directory, imagefilename))
        im = im.resize((300, 300))
        im.save(os.path.join(img_directory, imagefilename))
        
        print(f"Generated image and saved as '{imagefilename}'.")
    except Exception as e:
        print(f"Failed to generate image: {e}")

# Download the image to a local file
def download_image(image_url, local_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image from {image_url}")

# Main function to check images and generate them if necessary
def main():
    categories = load_yaml_file('categories.yaml')
    
    for category in categories['categories']:
        for prompt in category['prompts']:
            imagefilename = prompt['imagefilename']
            if not image_exists(imagefilename):
                print(f"\nImage file '{imagefilename}' needs to be generated.")
                user_prompt = input("Please enter the prompt for this image: ")
                dall_e_prompt = f"generate a dark mode retro pixel art style image containing no text of {user_prompt}"
                print(f"\nGenerating image with prompt: {dall_e_prompt}")
                generate_image(dall_e_prompt, imagefilename)

if __name__ == '__main__':
    main()
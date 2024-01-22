import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
import requests
from PIL import Image

# Load environment variables from a .env file located in the same directory as this script
load_dotenv()

# # Set OpenAI API key
# OpenAI.api_key = os.getenv('OPENAI_API_KEY')

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
        
        print(f"Generated image for '{prompt_text}' and saved as '{imagefilename}'.")
    except Exception as e:
        print(f"Failed to generate image for prompt '{prompt_text}': {e}")

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
            print(f"Checking image for prompt: {prompt['prompt']}")
            imagefilename = prompt['imagefilename']
            if not image_exists(imagefilename):
                # Generate a dark mode retro pixel image using the DALL-E 3 API
                dall_e_prompt = f"generate a dark mode retro pixel art style image containing no text of the entity whose job description is: {prompt['prompt']}."
                print(f"Image '{imagefilename}' not found, generating with prompt: {dall_e_prompt}")
                generate_image(dall_e_prompt, imagefilename)

if __name__ == '__main__':
    main()

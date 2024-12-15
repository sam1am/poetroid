from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import ollama
import base64
import uvicorn
import os
from datetime import datetime
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs('./uploads', exist_ok=True)
os.makedirs('./logs', exist_ok=True)

def log_interaction(filename: str, poem: str):
    """Log the interaction details to a file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"""
Timestamp: {timestamp}
Filename: {filename}
Poem:
{poem}
----------------------------------------
"""
    with open('./logs/poetroid.log', 'a') as f:
        f.write(log_entry)

@app.post("/generate_poem")
async def generate_poem(prompt: str = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to generate a poem about an image based on the given prompt
    """
    try:
        # Create unique filename
        unique_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        file_path = os.path.join('./uploads', unique_filename)
        
        # Save the uploaded file
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Convert to base64 for ollama
        base64_image = base64.b64encode(content).decode('utf-8')
        
        # Send image and prompt to llama
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': f"Using this image as inspiration, {prompt}",
                'images': [base64_image]
            }]
        )
        
        poem_text = response['message']['content']
        
        # Log the interaction
        log_interaction(unique_filename, poem_text)
        
        return {"response": poem_text}
    except Exception as e:
        print(f"Error: {str(e)}")  # Server-side logging
        return {"error": str(e)}, 500

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3090)
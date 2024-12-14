from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import ollama
import base64
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_poem")
async def generate_poem(prompt: str = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to generate a poem about an image based on the given prompt
    """
    try:
        # Read the image file
        image_data = await file.read()
        
        # Convert to base64 for ollama
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Send image and prompt to llama
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': f"Using this image as inspiration, {prompt}",
                'images': [base64_image]
            }]
        )
        
        return {"response": response['message']['content']}
    except Exception as e:
        print(f"Error: {str(e)}")  # Server-side logging
        return {"error": str(e)}, 500

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3090)
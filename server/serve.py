from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
import uuid
import base64
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Qwen3VLChatHandler

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
os.makedirs('./models', exist_ok=True)

# Model paths - Qwen3-VL-32B-Instruct GGUF
MODEL_PATH = "./models/Qwen3VL-2B-Instruct-F16.gguf"
MMPROJ_PATH = "./models/mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf"

# Initialize model and processor at startup
print("Loading Qwen3-VL-32B-Instruct model with llama.cpp...")
print(f"Model: {MODEL_PATH}")
print(f"MMProj: {MMPROJ_PATH}")

# Initialize chat handler with vision projector
chat_handler = Qwen3VLChatHandler(clip_model_path=MMPROJ_PATH)

# Load model with Q4_K_M quantization
llm = Llama(
    model_path=MODEL_PATH,
    chat_handler=chat_handler,
    n_ctx=4096,  # Context window for vision + text
    n_gpu_layers=-1,  # Use all GPU layers (set to 0 for CPU-only)
    verbose=False
)
print("Model loaded successfully!")

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

        # Convert image to base64 data URI for llama.cpp
        base64_image = base64.b64encode(content).decode('utf-8')

        # Determine image mimetype
        ext = os.path.splitext(file.filename)[1].lower()
        mime_type = "image/jpeg" if ext in ['.jpg', '.jpeg'] else "image/png"
        data_uri = f"data:{mime_type};base64,{base64_image}"

        # Create chat completion with image
        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": data_uri}
                        },
                        {
                            "type": "text",
                            "text": f"Using this image as inspiration, {prompt}"
                        }
                    ]
                }
            ],
            max_tokens=512,
            temperature=0.7,
            top_p=0.8,
            top_k=20,
        )

        poem_text = response['choices'][0]['message']['content']

        # Log the interaction
        log_interaction(unique_filename, poem_text)

        return {"response": poem_text}
    except Exception as e:
        print(f"Error: {str(e)}")  # Server-side logging
        return {"error": str(e)}, 500

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3090)

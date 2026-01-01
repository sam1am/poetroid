#!/usr/bin/env python3
"""
Download Qwen3-VL-32B-Instruct GGUF models from Hugging Face
"""
import os
from huggingface_hub import hf_hub_download

# Ensure models directory exists
os.makedirs('./models', exist_ok=True)

# Model repository and files
# REPO_ID = "Qwen/Qwen3-VL-32B-Instruct-GGUF"
# REPO_ID = "Qwen/Qwen3-VL-30B-A3B-Instruct-GGUF"
# REPO_ID = "Qwen/Qwen3-VL-8B-Instruct-GGUF"
# REPO_ID = "Qwen/Qwen3-VL-4B-Instruct-GGUF"
REPO_ID = "Qwen/Qwen3-VL-2B-Instruct-GGUF"

# Files to download
FILES = {
    # "Qwen3VL-32B-Instruct-Q4_K_M.gguf": "Q4_K_M quantized model (19.8 GB)",
    # "mmproj-Qwen3VL-32B-Instruct-Q8_0.gguf": "Q8_0 vision encoder (772 MB)"
    # "Qwen3VL-30B-A3B-Instruct-Q4_K_M.gguf": "QwenVL-30B Q4_K_M quantized model (18.6 GB)",
    # "mmproj-Qwen3VL-30B-A3B-Instruct-Q8_0.gguf": "QwenVL-30B Q8_0 vision encoder (712 MB)"
    # "Qwen3VL-8B-Instruct-Q8_0.gguf": "QwenVL-8B",
    # "mmproj-Qwen3VL-8B-Instruct-F16.gguf": "QwenVL-8B F16"
    # "Qwen3VL-4B-Instruct-F16.gguf": "QwenVL-4B F16",
    # "mmproj-Qwen3VL-4B-Instruct-F16.gguf": "QwenVL-4B F16"
    # "Qwen3VL-2B-Instruct-F16.gguf": "QwenVL-2B F16",
    "mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf": "QwenVL-2B F16"
}

print("Starting download of GGUF models...")
print(f"Repository: {REPO_ID}")
print("-" * 60)

for filename, description in FILES.items():
    print(f"\nDownloading {filename}")
    # print(f"Description: {description}")

    try:
        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            local_dir="./models",
            local_dir_use_symlinks=False
        )
        print(f"✓ Successfully downloaded to: {downloaded_path}")
    except Exception as e:
        print(f"✗ Error downloading {filename}: {str(e)}")

print("\n" + "=" * 60)
print("Download complete!")
print("\nModel files location: ./models/")
print("\nYou can now start the server with: python serve.py")

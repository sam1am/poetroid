# Poetroid 📸✍️

Welcome to the whimsical world of Poetroid, where technology waltzes with words! Morph the mundane memory-catcher into a mosaic maker of metaphors, marshaling mementos not in megapixels but in mellifluous meter. 

![Poetroid Device](./poetroid_device/poetroid_device.png)  

Call out "camembert," and collect your chronicles in crafted couplets!

## What's Poetroid?

Imagine capturing moments not in pixels, but in stanzas. With Poetroid, every snapshot becomes an ode, a sonnet, or a haiku. Crafted from a lunchbox, this little marvel uses self-hosted multi-modal models to peek into the soul of your surroundings and pen poems just for you.

🎚 Dial a Poet: Twist the top-side dial to select your poet.
🖨 Print Poetic Visions: Each poem is instantly printed out on a thermal prinr for you to keep, scrapbook, or pin to the refrigerator.
🔧 Off-the-shelf Heart: Built with accessible, DIY-friendly parts and a whole lot of love for the whole lot of you.

## Build your own

Learn AI! Finally impress your father! 

Full build instructions are on Hackaday here: https://hackaday.io/project/194632-poetroid-poetry-capturing-camera

Poetroid consists of two parts: Server and Client. 

### Client Camera Device

The client is the camera (pictured above). It is powered by a Single Board Computer (SBC) running Linux and the software from the ./poetroid_device folder in this repo. 

*Installation:*

```bash
git clone https://github.com/sam1am/poetroid
cd poetroid/poetroid_debices
python3 -m venv poetroid-venv
source poetroid-venv/bin/activate
pip install -r requirements.txt
python poetroid_app.py
```

### Server 

The server software (coming soon) can be run locally on the SBC (currently slow), or remotely on a more powerful machine with a GPU. 

## Parts and Libraries

Poetroid relies on a series of open-source libraries and models including:

- Tkinter
- Ollama
- PIL (Python Imaging Library)
- Llava (For vision. Configurable)
- Mistral (For poertry. Configurable)

Special thanks to the various open-source machine learning models (LLMs) and the supportive community on the `localllama` subreddit.

## License
The heartcrafted code of Poetroid pirouettes under the Apache License 2.0.
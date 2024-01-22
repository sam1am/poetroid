# check for venv folder, if it does not exist, create it
if [ ! -d "venv" ]; then
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

./venv/bin/python3 main_tk.py
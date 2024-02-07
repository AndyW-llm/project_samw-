from pynput import keyboard
# from operate.utils.text_util import copy_text_from_current_window

def default_action():
    text = ""
    # text = copy_text_from_current_window()
    print("[function activated] copied from selection:\n", text)

class KeyboardListener:
    def __init__(self, hotkey='<cmd>+`', action=default_action):
        self.listener = keyboard.GlobalHotKeys({
            hotkey: self.action,
        })
        self.action_fn = action
    
    def action(self):
        self.action_fn()
        self.stop_listener()

    def stop_listener(self):
        self.listener.stop()

    def run(self):
        with self.listener:
            self.listener.join()

# Example usage
if __name__ == "__main__":
    hotkey='<cmd>+`'
    print(f"KeyboardListener:\n  press {hotkey} to activate.\n  press <ctrl>+c to quit.")
    while True:
        print("-"*25)
        print("listener on")
        listener = KeyboardListener(hotkey=hotkey)
        listener.run()
        print("listener done")

import streamlit as st
import pyperclip
import pyautogui
import time
from operate.utils.keyboard_listener import KeyboardListener

def cmd_c():
    # Simulate Cmd+C (copy)
    pyautogui.keyDown('command')
    pyautogui.keyDown('c')
    time.sleep(0.1)
    pyautogui.keyUp('c')
    pyautogui.keyUp('command')

# setup/update cached content
if 'text' not in st.session_state:
    st.session_state.text = ""
    # TODO: set up index
else:
    st.session_state.text = pyperclip.paste()
    # TODO: conduct search with llama_index
    # st.markdown('''Happy Streamlit-ing! :balloon:''')
st.write(f"Content:  \n{st.session_state.text}")
hotkey='<cmd>+`'
st.write(f"[instruction] press {hotkey}` to initialize procedure.")
listener = KeyboardListener(hotkey=hotkey, action=cmd_c) 
# wait for `hotkey`, then do action 
listener.run()
# rerun
st.rerun()


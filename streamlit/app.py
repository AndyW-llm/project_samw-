import os
import streamlit as st
import pyperclip
import pyautogui
import time
from dotenv import load_dotenv
from operate.utils.keyboard_listener import KeyboardListener
from operate.llama_index.query import retrieve, get_query_engine

def cmd_c():
    # Simulate Cmd+C (copy)
    pyautogui.keyDown('command')
    pyautogui.keyDown('c')
    time.sleep(0.1)
    pyautogui.keyUp('c')
    pyautogui.keyUp('command')

def get_contents(text, engine, index_mode = "bm25"):
    SEARCH_PROMPT = """
    {text}
    """
    _, source_nodes = retrieve(
        llama_idx_engine = engine,
        prompt = SEARCH_PROMPT.format(text=text),
        index_mode = index_mode,
    )
    contents = []
    seen = set()
    # TODO: improve with map?
    for content in source_nodes:
        file_path= content.metadata["file_path"]
        if file_path in seen:   continue

        dir_path = os.path.dirname(file_path)
        folder_name = os.path.basename(dir_path)
        file_name = os.path.basename(file_path)
        py_file_path = os.path.join(dir_path, f"{folder_name}.py")
        pyqueue = []
        
        if not file_name.endswith(".py"):
            contents.append({
                "title": os.sep.join([folder_name, file_name]),
                # "path": file_path,
                "text": content.text,
            })
            seen.add(file_path)
        else:
            pyqueue.append(file_path)
        
        if file_name == "README.md" and \
            os.path.isfile(py_file_path) and \
            (not py_file_path in seen) and \
            (not py_file_path in pyqueue):
            pyqueue.append(py_file_path)

        for pyqueue_file_path in pyqueue:
            with open(pyqueue_file_path, "r") as file:
                py_code = file.read()
            contents.append({
                "title": os.path.basename(pyqueue_file_path),
                # "path": py_file_path,
                "text": "```python\n{code}\n```\n".format(code=py_code),
            })
            seen.add(pyqueue_file_path)
    return contents


# setup/update cached content
if 'text' not in st.session_state:
    load_dotenv()
    st.session_state.text = ""
    st.session_state.query_engine = get_query_engine(
        knowledge_dir = os.getenv("KNOWLEDGE_PATH"),
        index_dir = os.getenv("INDEX_PATH"),
        knowledge = "leethub_v2",
        response_mode = "no_text",
        streaming = False,
        index_mode = "bm25",
    )
    st.markdown("---")
else:
    st.session_state.text = pyperclip.paste()
    contents = get_contents(
        st.session_state.text, 
        engine=st.session_state.query_engine,
        index_mode = "bm25",
        )
    for content in contents:
        st.markdown('''#  {title}\n{text}'''.format(title=content["title"], text=content["text"]))
        st.markdown("---")
st.write(f"Content:  \n{st.session_state.text}")
hotkey='<cmd>+`' #'<ctrl>+<alt>+<cmd>'
st.markdown("---")
st.write(f"[instruction] press {hotkey} to initialize procedure.")
listener = KeyboardListener(hotkey=hotkey, action=cmd_c) 
# wait for `hotkey`, then do action 
listener.run()
# rerun
st.rerun()


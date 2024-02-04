# import os
# import platform
# import subprocess
import pyautogui
import pyperclip
import time

def copy_text_from_current_window(
        time_pause=0.1, 
        manual_highlight=True,
        manual_copy=False,
    ):
    """
    # Example usage
    # text = copy_text_from_current_window()
    """
    # TODO: try keystrokes logging.

    if not manual_highlight:
        # Simulate Cmd+A (select all)
        pyautogui.keyDown('command')
        pyautogui.press('a')
        pyautogui.keyUp('command')
        time.sleep(time_pause)  # Wait for the selection to complete
    
    if not manual_copy:
        # Simulate Cmd+C (copy)
        pyautogui.keyDown('command')
        pyautogui.keyDown('c')
        # pyautogui.press('c')
        time.sleep(time_pause)
        pyautogui.keyUp('c')
        pyautogui.keyUp('command')
        time.sleep(time_pause)  # Wait for the copy to complete

    # click cursor again to remove the highlighta
    if not manual_highlight:
        pyautogui.click()

    # Get text from clipboard
    # print("DEBUG: copy_text_from_current_window")
    # print(pyperclip.paste())
    # print("exiting: copy_text_from_current_window")

    return pyperclip.paste()


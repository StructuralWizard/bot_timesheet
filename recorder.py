import sys
import os
import time
import pyautogui
import keyboard
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from threading import Thread
from PIL import ImageGrab

# Create commands directory if it doesn't exist
os.makedirs("comandos", exist_ok=True)

running = True  # Shared flag to control the loop and listeners
action_counter = 1  # Unique counter for all actions
last_action_time = time.time()  # Time of the last action

# Variables for button capture process
button_capture_mode = False
xclick, yclick = 0, 0
xtl, ytl = 0, 0
xlr, ylr = 0, 0
capture_step = 0  # 0=not capturing, 1=click registered, 2=top-left registered

# Variables for text and scroll grouping
current_text = ""
scroll_count = 0
last_text_time = 0
last_scroll_time = 0

def save_text_action():
    global current_text, action_counter, last_text_time
    if current_text:
        delay = round(time.time() - last_action_time, 1)
        filename = f"comandos/{action_counter:03d}_texto_t{delay}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(current_text)
        print(f"Saved text to {filename}")
        current_text = ""
        action_counter += 1
        last_text_time = 0

def save_scroll_action():
    global scroll_count, action_counter, last_scroll_time
    if scroll_count:
        delay = round(time.time() - last_action_time, 1)
        filename = f"comandos/{action_counter:03d}_scroll_t{delay}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{scroll_count}")
        print(f"Saved scroll to {filename}")
        scroll_count = 0
        action_counter += 1
        last_scroll_time = 0

def on_press(key):
    global running, last_action_time, current_text, last_text_time
    global button_capture_mode, capture_step, xclick, yclick, xtl, ytl, xlr, ylr, action_counter
    
    # Check for F10 (stop recording)
    if hasattr(key, 'name') and key.name == 'f10':
        print("Stopping the recording...")
        # Save any pending actions
        save_text_action()
        save_scroll_action()
        running = False
        return False  # Stop listener
    
    # Check for F8 (start button capture)
    elif hasattr(key, 'name') and key.name == 'f8':
        if not button_capture_mode or capture_step == 0:
            x, y = pyautogui.position()
            xclick, yclick = x, y
            capture_step = 1
            button_capture_mode = True
            print(f"Button position saved: ({xclick}, {yclick})")
            print("Now position cursor at the top-left corner of the button and press F9")
        return True
    
    # Check for F9 (continue button capture)
    elif hasattr(key, 'name') and key.name == 'f9':
        if button_capture_mode:
            if capture_step == 1:
                xtl, ytl = pyautogui.position()
                capture_step = 2
                print(f"Top-left corner saved: ({xtl}, {ytl})")
                print("Now position cursor at the bottom-right corner of the button and press F9")
            elif capture_step == 2:
                xlr, ylr = pyautogui.position()
                print(f"Bottom-right corner saved: ({xlr}, {ylr})")
                
                # Calculate offsets
                x_offset = int(xclick - (xtl + xlr) / 2)
                y_offset = int(yclick - (ytl + ylr) / 2)
                
                # Take screenshot and crop
                screenshot = ImageGrab.grab()
                button_image = screenshot.crop((xtl, ytl, xlr, ylr))
                
                # Save the image
                delay = round(time.time() - last_action_time, 1)
                filename = f"comandos/{action_counter:03d}_boton_x{x_offset}_y{y_offset}_t{delay}.bmp"
                button_image.save(filename)
                print(f"Button screenshot saved to {filename}")
                
                # Reset capture mode
                button_capture_mode = False
                capture_step = 0
                action_counter += 1
                last_action_time = time.time()
        return True
    
    # Don't record function keys
    if hasattr(key, 'name') and key.name.startswith('f'):
        return True
    
    # Save any pending scroll action
    if scroll_count > 0:
        save_scroll_action()
    
    # Get current time for grouping logic
    current_time = time.time()
    
    # Start a new text group if this is the first keystroke or if time gap is significant
    if last_text_time == 0 or current_time - last_text_time > 1.5:
        save_text_action()  # Save any previous text
        last_action_time = current_time
    
    # Update the last text time
    last_text_time = current_time
    
    # Handle all types of keys properly
    if hasattr(key, 'char') and key.char is not None:
        # Regular character key
        current_text += key.char
    else:
        # Special key handling
        key_str = str(key)
        if key_str == 'Key.space':
            current_text += " "
        elif key_str == 'Key.enter':
            current_text += "\n"
        elif key_str == 'Key.tab':
            current_text += "\t"
        elif key_str == 'Key.backspace' and current_text:
            current_text = current_text[:-1]
        # Skip recording other special keys like shift, ctrl, alt
        elif key_str in ('Key.shift', 'Key.shift_r', 'Key.shift_l', 
                         'Key.ctrl', 'Key.ctrl_r', 'Key.ctrl_l',
                         'Key.alt', 'Key.alt_r', 'Key.alt_l',
                         'Key.cmd', 'Key.cmd_r', 'Key.cmd_l'):
            pass
    
    return True

def on_click(x, y, button, pressed):
    if button_capture_mode:
        return True  # Don't process regular clicks during button capture
    
    if pressed:
        # Save any pending actions
        save_text_action()
        save_scroll_action()
        #print(f'Mouse clicked at ({x}, {y}) with {button}')
    
    return True  # Continue listening

def on_scroll(x, y, dx, dy):
    global scroll_count, last_scroll_time, last_action_time
    
    # Save any pending text action
    if current_text:
        save_text_action()
    
    # Start a new scroll group if this is the first scroll or if time gap is significant
    current_time = time.time()
    if last_scroll_time == 0 or current_time - last_scroll_time > 1.5:
        save_scroll_action()  # Save any previous scroll
        last_action_time = current_time
    
    # Count scrolls with proper scaling for pyautogui
    # pynput uses dy=1 for upward scroll, while pyautogui uses positive values for upward scroll
    # Multiply by 100 to scale appropriately for pyautogui (which needs larger values)
    scroll_count += int(dy * 30)
    last_scroll_time = current_time
    
    #print(f'Mouse scrolled at ({x}, {y})({dx}, {dy})')
    return True

def on_move(x, y):
    if not button_capture_mode:  # Only log movement when not in button capture mode
        pass
        #print(f"Mouse moved to ({x}, {y})")
    return True

def stop_recording():
    global running
    # Save any pending actions
    save_text_action()
    save_scroll_action()
    running = False

# Start the listeners
keyboard_listener = KeyboardListener(on_press=on_press)
mouse_listener = MouseListener(on_click=on_click, on_scroll=on_scroll, on_move=on_move)

print("Recording started. Press F10 to stop.")
print("F8 to start capturing a button (first click where you want to click the button)")
print("F9 to mark top-left and bottom-right corners of the button")

keyboard_listener.start()
mouse_listener.start()

# Main loop to keep the program running
try:
    while running:
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_recording()

# Ensure listeners are stopped
keyboard_listener.stop()
mouse_listener.stop()
print("Recording stopped.")
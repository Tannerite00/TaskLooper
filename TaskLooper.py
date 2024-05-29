import tkinter as tk
from tkinter import messagebox
from pynput import mouse, keyboard
import threading
import time

# Global variables to store events and control flags
recorded_events = []
recording = False

# Start recording mouse and keyboard events
def start_recording():
    global recording, recorded_events
    if recording:
        messagebox.showinfo("Info", "Already recording!")
        return

    recording = True
    recorded_events = []
    
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    mouse_listener.start()
    keyboard_listener.start()
    
    mouse_listener.join()
    keyboard_listener.join()

# Stop recording
def stop_recording():
    global recording
    recording = False

# Callback functions to capture events
def on_click(x, y, button, pressed):
    if recording:
        recorded_events.append(('mouse_click', x, y, button, pressed))

def on_move(x, y):
    if recording:
        recorded_events.append(('mouse_move', x, y))

def on_press(key):
    if recording:
        recorded_events.append(('key_press', key))
    if key == keyboard.Key.f12:
        stop_recording()

def on_release(key):
    if recording:
        recorded_events.append(('key_release', key))

# Replay recorded events
def replay_events():
    for event in recorded_events:
        if event[0] == 'mouse_click':
            x, y, button, pressed = event[1], event[2], event[3], event[4]
            if pressed:
                mouse_controller.press(button)
            else:
                mouse_controller.release(button)
            mouse_controller.position = (x, y)
        elif event[0] == 'mouse_move':
            x, y = event[1], event[2]
            mouse_controller.position = (x, y)
        elif event[0] == 'key_press':
            key = event[1]
            keyboard_controller.press(key)
        elif event[0] == 'key_release':
            key = event[1]
            keyboard_controller.release(key)
        time.sleep(0.01)

# GUI setup
def create_gui():
    window = tk.Tk()
    window.title("Event Recorder")

    start_button = tk.Button(window, text="Start Recording", command=lambda: threading.Thread(target=start_recording).start())
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop Recording (F12)", command=stop_recording)
    stop_button.pack(pady=10)

    replay_button = tk.Button(window, text="Replay Events", command=lambda: threading.Thread(target=replay_events).start())
    replay_button.pack(pady=10)

    window.mainloop()

# Controllers for mouse and keyboard
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

# Run the GUI
if __name__ == "__main__":
    create_gui()

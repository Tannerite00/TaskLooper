import tkinter as tk
from tkinter import messagebox, filedialog
from pynput import mouse, keyboard
import threading
import time
import json

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
        event = ('mouse_click', x, y, str(button), pressed)
        recorded_events.append(event)
        listbox.insert(tk.END, event)

def on_move(x, y):
    if recording:
        event = ('mouse_move', x, y)
        recorded_events.append(event)
        listbox.insert(tk.END, event)

def on_press(key):
    if recording:
        event = ('key_press', str(key))
        recorded_events.append(event)
        listbox.insert(tk.END, event)
    if key == keyboard.Key.f12:
        stop_recording()

def on_release(key):
    if recording:
        event = ('key_release', str(key))
        recorded_events.append(event)
        listbox.insert(tk.END, event)

# Replay recorded events
def replay_events():
    for event in recorded_events:
        if event[0] == 'mouse_click':
            _, x, y, button, pressed = event
            button = mouse.Button[button.split('.')[-1]]
            if pressed:
                mouse_controller.press(button)
            else:
                mouse_controller.release(button)
            mouse_controller.position = (x, y)
        elif event[0] == 'mouse_move':
            _, x, y = event
            mouse_controller.position = (x, y)
        elif event[0] == 'key_press':
            _, key = event
            key = keyboard.Key[key.split('.')[-1]] if 'Key' in key else key.strip("'")
            keyboard_controller.press(key)
        elif event[0] == 'key_release':
            _, key = event
            key = keyboard.Key[key.split('.')[-1]] if 'Key' in key else key.strip("'")
            keyboard_controller.release(key)
        time.sleep(0.01)

# Save events to a file
def save_events():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(recorded_events, file)
        messagebox.showinfo("Info", "Events saved successfully!")

# Load events from a file
def load_events():
    global recorded_events
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            recorded_events = json.load(file)
        listbox.delete(0, tk.END)
        for event in recorded_events:
            listbox.insert(tk.END, event)
        messagebox.showinfo("Info", "Events loaded successfully!")

# Delete selected event
def delete_event():
    selected_indices = listbox.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            listbox.delete(index)
            del recorded_events[index]

# GUI setup
def create_gui():
    global listbox
    window = tk.Tk()
    window.title("Event Recorder")

    frame = tk.Frame(window)
    frame.pack(pady=10)

    start_button = tk.Button(frame, text="Start Recording", command=lambda: threading.Thread(target=start_recording).start())
    start_button.grid(row=0, column=0, padx=5)

    stop_button = tk.Button(frame, text="Stop Recording (F12)", command=stop_recording)
    stop_button.grid(row=0, column=1, padx=5)

    replay_button = tk.Button(frame, text="Replay Events", command=lambda: threading.Thread(target=replay_events).start())
    replay_button.grid(row=0, column=2, padx=5)

    save_button = tk.Button(frame, text="Save Events", command=save_events)
    save_button.grid(row=1, column=0, padx=5)

    load_button = tk.Button(frame, text="Load Events", command=load_events)
    load_button.grid(row=1, column=1, padx=5)

    delete_button = tk.Button(frame, text="Delete Event", command=delete_event)
    delete_button.grid(row=1, column=2, padx=5)

    listbox = tk.Listbox(window, width=100, height=20)
    listbox.pack(pady=10)

    window.mainloop()

# Controllers for mouse and keyboard
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

# Run the GUI
if __name__ == "__main__":
    create_gui()

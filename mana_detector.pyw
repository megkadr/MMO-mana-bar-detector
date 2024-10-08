import cv2
import pyautogui
import numpy as np
import os
from datetime import datetime
import threading
import tkinter as tk
from tkinter import ttk

# Configuration
SAVE_DIR = r'C:\Path\To\Your\Debug\Folder'
MANA_BAR = {
    'x1': 115,
    'x2': 370,
    'y1': 103,
    'y2': 130,
}
MANA_THRESHOLD = 0.7
MANA_HOTKEY = '-'
CHECK_INTERVAL = 1.0
DEBUG_MODE = True

# Global variables
running = True

def create_debug_directory():
    if DEBUG_MODE:
        os.makedirs(os.path.dirname(SAVE_DIR), exist_ok=True)

def save_debug_image(image, name):
    if DEBUG_MODE:
        try:
            cv2.imwrite(SAVE_DIR, image)
        except Exception as e:
            print(f"Failed to save debug image: {e}")

def check_mana_level(screenshot):
    # Extract mana bar region
    mana_bar_region = screenshot[MANA_BAR['y1']:MANA_BAR['y2'], 
                                MANA_BAR['x1']:MANA_BAR['x2']]
    
    if DEBUG_MODE:
        save_debug_image(mana_bar_region, "mana_bar_region")
    
    # Convert to HSV for better blue detection
    hsv = cv2.cvtColor(mana_bar_region, cv2.COLOR_BGR2HSV)
    
    # Define range for blue color of mana
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    # Create mask for blue pixels
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    if DEBUG_MODE:
        save_debug_image(blue_mask, "blue_mask")
    
    # Find the rightmost blue pixel for each row
    max_x_positions = []
    height, width = blue_mask.shape
    
    for y in range(height):
        row = blue_mask[y]
        blue_positions = np.where(row > 0)[0]
        if len(blue_positions) > 0:
            max_x_positions.append(max(blue_positions))
    
    if max_x_positions:
        avg_max_x = sum(max_x_positions) / len(max_x_positions)
        mana_percentage = avg_max_x / width
        
        if DEBUG_MODE:
            debug_image = mana_bar_region.copy()
            cv2.line(debug_image, (int(avg_max_x), 0), 
                    (int(avg_max_x), height), (0, 255, 0), 1)
            save_debug_image(debug_image, "mana_debug_line")
        
        return mana_percentage
    return 0

def mana_check_loop(status_label):
    global running
    while running:
        try:
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            
            mana_level = check_mana_level(screenshot)
            
            status_text = f"Mana level: {mana_level * 100:.2f}%"
            status_label.config(text=status_text)
            
            if mana_level < MANA_THRESHOLD:
                pyautogui.press(MANA_HOTKEY)
                if DEBUG_MODE:
                    print(f"Mana low! Pressed {MANA_HOTKEY}")
            
            # Use root.after to update GUI every 100ms
            for _ in range(10):  # Split CHECK_INTERVAL into smaller chunks
                if not running:
                    break
                root.after(int(CHECK_INTERVAL * 100))
                
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
            root.after(1000)  # Wait a second before retrying

def stop_script():
    global running
    running = False
    root.quit()

# Create GUI
root = tk.Tk()
root.title("Mana Detection")
root.geometry("300x150")
root.attributes('-topmost', True)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

status_label = ttk.Label(frame, text="Starting...", wraplength=250)
status_label.grid(row=0, column=0, pady=10)

stop_button = ttk.Button(frame, text="Stop Script", command=stop_script)
stop_button.grid(row=1, column=0, pady=10)

def main():
    create_debug_directory()
    
    # Start mana check in a separate thread
    mana_thread = threading.Thread(target=mana_check_loop, args=(status_label,), daemon=True)
    mana_thread.start()
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
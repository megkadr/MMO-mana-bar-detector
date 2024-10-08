# Auto Mana Skill Activator

A Python script that automatically activates a specified hotkey when your in-game mana bar falls below 70%. Perfect for MMORPGs where mana management is crucial.

## Description
This script continuously monitors a specified area of your screen where the mana bar is located. When the blue portion of the mana bar indicates less than 70% mana remaining, it automatically presses a predefined hotkey (default is '-').

## Prerequisites
Before running this script, you need to:
1. Install Python 3.7 or higher from [Python's official website](https://www.python.org/downloads/)
2. Install required libraries using pip (Python's package installer)

## Installation

1. **Install required libraries**
   Open Command Prompt (CMD) and run:
   ```
   pip install opencv-python numpy pyautogui tkinter
   ```

2. **Download the script**
   - Download the script file and save it with a `.pyw` extension (e.g., `mana_detector.pyw`)

## Configuration

### Mana Bar Measurement
You need to adjust the mana bar coordinates for your screen resolution:

1. Take a screenshot of your game
2. Open the screenshot in an image editor (like Paint)
3. Move your cursor to find these coordinates:
   - Left edge of mana bar (x1)
   - Right edge of mana bar (x2)
   - Top edge of mana bar (y1)
   - Bottom edge of mana bar (y2)
4. Update these values in the script:
   ```python
   MANA_BAR = {
       'x1': 115,  # Replace with your left edge coordinate
       'x2': 370,  # Replace with your right edge coordinate
       'y1': 103,  # Replace with your top edge coordinate
       'y2': 130,  # Replace with your bottom edge coordinate
   }
   ```

### Optional Settings
- `MANA_THRESHOLD = 0.7` - Change `0.7` to adjust at what mana percentage the script activates
- `MANA_HOTKEY = '-'` - Change `'-'` to your desired hotkey
- `CHECK_INTERVAL = 1.0` - Change `1.0` to adjust how often the script checks mana (in seconds)

## Running the Script

1. **Method 1: Direct Run**
   - Double click the script file (`.pyw`)

2. **Method 2: Create a Shortcut (Recommended)**
   - Right-click the script file
   - Select "Create shortcut"
   - Right-click the shortcut and select "Properties"
   - In the "Shortcut key" field, set a keyboard shortcut (e.g., Ctrl+Alt+M)

When running, a small window will appear with:
- Current mana level
- A "Stop" button to close the script

## Stopping the Script
Click the "Stop" button in the script's window.

## Troubleshooting

1. **Script not detecting mana correctly**
   - Verify your mana bar coordinates
   - Try adjusting the blue color range in the script
   - Make sure your game's mana bar is visible and not covered

2. **Script not starting**
   - Ensure all required libraries are installed
   - Try running from Command Prompt to see error messages

## Disclaimer
Use of this script should comply with your game's terms of service. Use at your own risk.

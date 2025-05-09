# Bot Timesheet

A Python automation tool that helps fill out timesheets by simulating mouse clicks, keyboard input, and scrolling actions based on pre-defined commands.

## Features

- **Automated Button Clicking**: Finds and clicks buttons on the screen using image recognition
- **Text Input Automation**: Automatically types text from text files
- **Mouse Scroll Simulation**: Simulates mouse wheel scrolling
- **Action Recording**: Includes a recorder utility to create automation sequences

## Project Components

- **bot_timesheet.py**: Main script that executes the automated actions
- **recorder.py**: Utility to record mouse clicks, keyboard input, and scrolling actions
- **comandos/**: Directory containing all the command files (images, text files) used by the bot

## How It Works

### Command Types

1. **Button Commands**: Stored as `.bmp` files in the format `<order>_boton_x<x_offset>_y<y_offset>_t<delay>.bmp`
   - These are button images the bot will look for on screen
   - x_offset and y_offset define the click position relative to the button's center
   - t<delay> specifies how long to wait after clicking

2. **Text Commands**: Stored as `.txt` files in the format `<order>_texto_t<delay>.txt`
   - These contain text the bot will type
   - Before typing, it selects all existing text (Ctrl+A) and deletes it

3. **Scroll Commands**: Stored as `.txt` files in the format `<order>_scroll_t<delay>.txt`
   - These contain the scroll amount (positive for up, negative for down)

## Requirements

- Python 3.6+
- PyAutoGUI
- PIL (Pillow)
- keyboard
- pynput
- OpenCV-Python (for image recognition confidence)

## Installation

```bash
# Clone the repository
git clone https://github.com/StructuralWizard/bot_timesheet.git
cd bot_timesheet

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Bot

```bash
python bot_timesheet.py
```

The bot will:
1. Wait 3 seconds (to allow you to position your cursor)
2. Execute all commands in the `comandos` directory in alphabetical order

### Recording New Commands

```bash
python recorder.py
```

The recorder allows you to:
- Press F8 to record the position where you want to click
- Press F9 to mark the top-left and then bottom-right corners of the button
- Type to record keyboard input
- Use the scroll wheel to record scrolling
- Press F10 to stop recording

## Notes

- The image recognition uses OpenCV for reliability. If you encounter issues, adjust the `confidence` parameter in the code.
- For button clicks, make sure the button images are clear and distinctive.
- The bot runs actions in alphabetical order of the filenames, so naming conventions are important.

## License

This project is open source and available under the [MIT License](LICENSE).

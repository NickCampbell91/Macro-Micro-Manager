# Macro Micro Manager

Macro Micro Manager is a user-friendly, tkinter-based Python application designed for creating and executing custom macros consisting of mouse and keyboard actions. With an intuitive graphical interface, this powerful tool allows you to automate repetitive tasks, enhance productivity, and streamline your workflow by combining a series of mouse clicks, key presses, and wait times into a single macro.

## Features

- Create custom macro actions such as clicks, key presses, and wait times
- Add and remove actions
- Save and load macro configurations
- Execute macros using a custom hotkey combination (default is Ctrl + 1)
- Stop macro execution by using the hotkey again

## Instructions

1. Add a new row by clicking the 'New Row' button.
2. Select the action for the row in the dropdown menu.
   - Click: Clicks the mouse at the specified coordinates.
   - Press: Presses the specified key.
   - Wait: Waits for the specified amount of time.
   - Return: Resets the macro to the specified step.
3. Fill in the required fields for the selected action.
4. Click 'Execute' to run the macro.
5. Press 'Ctrl' + your hotkey (default is '1') to run the macro.
6. Click 'Stop' or press 'Esc' to stop the macro.
7. Save your macro by clicking 'File' > 'Save'.
8. Load a saved macro by clicking 'File' > 'Open'.

## Dependencies

- tkinter
- ttkthemes
- keyboard

## Usage

To use Macro Micro Manager, you can simply download and execute the EXE file or follow these steps:

1. Make sure you have Python installed on your system. If not, download it from [python.org](https://www.python.org/downloads/).
2. Install the required dependencies using the following command:

```
pip install tkinter ttkthemes keyboard
```
3. Clone the repository or download the source files.
4. Open a terminal or command prompt, navigate to the project directory, and run the main script:

```
python main.py
```
5. The Macro Micro Manager application window will open, and you can now start creating and executing macros.

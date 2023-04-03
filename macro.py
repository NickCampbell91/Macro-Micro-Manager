import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import time
import keyboard
from threading import Event
from file_manager import FileManager
from ttk_option_menu import TTKOptionMenu
from validators import Validator

class App:
    def __init__(self, master=None):
        self.root = root
        self.master = master if master else ThemedTk(theme="equilux")
        self.master.title("Macro Micro Manager")
        self.create_menu_bar()
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)
        self.dropdown_frame = ttk.Frame(self.root)
        self.dropdown_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.rows = []
        self.create_main_dropdown()
        self.create_buttons()
        self.hotkey = '1'  # Set the hotkey attribute before calling create_hotkey_input
        self.create_hotkey_input()
        self.stop_execution = False
        self.root.bind('<Escape>', self.stop_execution_callback)
        self.last_key = None
        self.held_buttons = set()
        self.keyboard = keyboard
        self.setup_hotkey()
        self.validator = Validator()

        style = ttk.Style()
        style.theme_use('equilux')

    # MENU-RELATED FUNCTIONS

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New", command=self.reset_rows)
        file_menu.add_command(label="Open", command=lambda: FileManager.load_from_file(self))
        file_menu.add_command(label="Save", command=lambda: FileManager.save_to_file(self.rows))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="Display Input", command=self.display_values)


    def show_instructions(self):
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instructions")

        instructions_text = (
            "1. Add a new row by clicking the 'New Row' button.\n"
            "2. Select the action for the row in the dropdown menu.\n"
            "   - Click: Clicks the mouse at the specified coordinates.\n"
            "   - Press: Presses the specified key.\n"
            "   - Wait: Waits for the specified amount of time.\n"
            "   - Return: Resets the macro to the spcified step.\n"
            "3. Fill in the required fields for the selected action.\n"
            "4. Click 'Execute' to run the macro.\n"
            "5. Press 'Ctrl' + your hotkey (default is '1') to run the macro.\n"
            "6. Click 'Stop' or press 'Esc' to stop the macro.\n"
            "7. Save your macro by clicking 'File' > 'Save'.\n"
            "8. Load a saved macro by clicking 'File' > 'Open'.\n"
        )

        instructions_label = ttk.Label(instructions_window, text=instructions_text, justify=tk.LEFT)
        instructions_label.pack(padx=10, pady=10)

    # ROW-RELATED FUNCTIONS

    def create_main_dropdown(self):
        main_var = tk.StringVar()
        main_var.trace('w', lambda *args, var=main_var: self.update_widgets(var))
        main_dropdown = TTKOptionMenu(self.dropdown_frame, main_var, 'Click', 'Press', 'Wait', 'Return')
        main_dropdown.grid(row=0, column=1)

        row = {"main_var": main_var, "main_dropdown": main_dropdown, "extra_widgets": []}
        self.rows.append(row)
        self.add_label(row, 1)  # Pass 1 as the row number for the first row

    def update_widgets(self, main_var):
        row = next((r for r in self.rows if r["main_var"] == main_var), None)
        if not row:
            return

        for widget in row["extra_widgets"]:
            widget.grid_forget()
        row["extra_widgets"].clear()

        selected = main_var.get()
        if selected == 'Press':
            self.add_press_options(row)
        elif selected == 'Wait':
            self.add_wait_options(row)
        elif selected == 'Return':
            self.add_return_options(row)


    def add_press_options(self, row):
        key_label = ttk.Label(self.dropdown_frame, text="Key:")
        key_label.grid(row=self.rows.index(row), column=2)
        row["extra_widgets"].append(key_label)

        key_entry = ttk.Entry(self.dropdown_frame, width=5)
        key_entry.grid(row=self.rows.index(row), column=3)
        row["extra_widgets"].append(key_entry)

        press_hold_var = tk.StringVar()
        press_hold_dropdown = TTKOptionMenu(self.dropdown_frame, press_hold_var, 'Press', 'Hold', 'Release')
        press_hold_dropdown.grid(row=self.rows.index(row), column=4)
        row["extra_widgets"].append(press_hold_dropdown)

    def add_wait_options(self, row):
        duration_label = ttk.Label(self.dropdown_frame, text="Duration (s):")
        duration_label.grid(row=self.rows.index(row), column=2)
        row["extra_widgets"].append(duration_label)

        entry = ttk.Entry(self.dropdown_frame, validate='key', validatecommand=(self.root.register(self.validator.validate_float), '%P'), width=5)
        entry.grid(row=self.rows.index(row), column=3)
        row["extra_widgets"].append(entry)

    def add_return_options(self, row):
        return_label = ttk.Label(self.dropdown_frame, text="Row:")
        return_label.grid(row=self.rows.index(row), column=2)
        row["extra_widgets"].append(return_label)

        entry = ttk.Entry(self.dropdown_frame, validate='key', validatecommand=(self.root.register(self.validator.validate_integer_range), '%P'), width=5)
        entry.grid(row=self.rows.index(row), column=3)
        row["extra_widgets"].append(entry)

        repetitions_label = ttk.Label(self.dropdown_frame, text="Repetitions:")
        repetitions_label.grid(row=self.rows.index(row), column=4)
        row["extra_widgets"].append(repetitions_label)

        repetitions_entry = ttk.Entry(self.dropdown_frame, validate='key', validatecommand=(self.root.register(self.validator.validate_non_negative_integer), '%P'), width=5)
        repetitions_entry.grid(row=self.rows.index(row), column=5)
        row["extra_widgets"].append(repetitions_entry)

    def add_row(self):
        main_var = tk.StringVar()
        main_var.trace('w', lambda *args, var=main_var: self.update_widgets(var))
        main_dropdown = TTKOptionMenu(self.dropdown_frame, main_var, 'Click', 'Press', 'Wait', 'Return')
        main_dropdown.grid(row=len(self.rows), column=1)

        row = {"main_var": main_var, "main_dropdown": main_dropdown, "extra_widgets": []}
        self.rows.append(row)
        self.add_label(row, len(self.rows))  # Pass the current row number

    def remove_row(self):
        if len(self.rows) > 1:
            row = self.rows.pop()
            row["main_dropdown"].grid_forget()
            row["label"].grid_forget()
            for widget in row["extra_widgets"]:
                widget.grid_forget()
            self.update_row_labels()

    def reset_rows(self):
        for row in self.rows:
            for widget in row["extra_widgets"]:
                widget.grid_forget()
            row["main_dropdown"].grid_forget()
            row["label"].grid_forget()

        self.rows.clear()
        self.create_main_dropdown()

    def update_row_labels(self):
        for index, row in enumerate(self.rows):
            if "label" not in row:
                row["label"] = ttk.Label(self.dropdown_frame, text="", font=("Arial", 12))
                row["label"].grid(row=index, column=0, padx=(10, 0), pady=(5, 5), sticky="w")
            row["label"].config(text=str(index + 1))

    # INPUT-RELATED FUNCTIONS

    def create_buttons(self):
        new_row_button = ttk.Button(self.button_frame, text="New Row", command=self.add_row)
        new_row_button.grid(row=0, column=0, padx=5, pady=5)

        remove_row_button = ttk.Button(self.button_frame, text="Remove Row", command=self.remove_row)
        remove_row_button.grid(row=0, column=1, padx=5, pady=5)

        execute_button = ttk.Button(self.button_frame, text="Execute", command=self.execute)
        execute_button.grid(row=0, column=2, padx=5, pady=5)

        stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_execution_button)
        stop_button.grid(row=0, column=3, padx=5, pady=5)

    # HOTKEY-RELATED FUNCTIONS

    def create_hotkey_input(self):
        hotkey_label = ttk.Label(self.button_frame, text="Hotkey (ctrl+):")
        hotkey_label.grid(row=0, column=4, padx=5, pady=5)

        hotkey_entry = ttk.Entry(self.button_frame, width=5)
        hotkey_entry.grid(row=0, column=5, padx=5, pady=5)
        hotkey_entry.insert(0, self.hotkey)
        hotkey_entry.bind('<FocusOut>', self.update_hotkey)

    def update_hotkey(self, event):
        keyboard.remove_hotkey(f'ctrl+{self.hotkey}') if self.hotkey else None
        self.hotkey = event.widget.get()
        self.setup_hotkey()

    def setup_hotkey(self):
        keyboard.add_hotkey(f'ctrl+{self.hotkey}', self.execute)

    # MACRO-RELATED FUNCTIONS

    def display_values(self):
        for row in self.rows:
            main_value = row["main_var"].get()
            extra_values = []

            for widget in row["extra_widgets"]:
                if isinstance(widget, ttk.Entry):
                    extra_values.append(widget.get())
                elif isinstance(widget, TTKOptionMenu):
                    extra_values.append(widget.var.get())

            print([main_value] + extra_values)

    def click(self, direction):
        if direction == 'Down':
            keyboard.press('left')
            keyboard.release('left')
        elif direction == 'Up':
            keyboard.press('right')
            keyboard.release('right')

    def press(self, key, action):
        # Convert key to the corresponding special key code
        special_key_map = {
            'Enter': 'enter',
            'ArrowUp': 'up',
            'ArrowDown': 'down',
            'ArrowLeft': 'left',
            'ArrowRight': 'right',
        }
        key = special_key_map.get(key, key)

        if action == 'Hold':
            keyboard.press(key)
        elif action == 'Release':
            keyboard.release(key)

    def stop_execution_button(self):
        self.stop_execution_callback(None)

    def stop_execution_callback(self, event):
        self.stop_execution = True
        self.release_held_buttons()  # Release held buttons before stopping the execution
        self.root.unbind('<Escape>')
        print("Execution stopped.")

    def release_held_buttons(self):
        for key in self.held_buttons:
            keyboard.release(key)
        self.held_buttons.clear()

    def set_label_color(self, row, color):
        row["label"].config(fg=color)

    def add_label(self, row_obj, row_number):
        row = self.rows.index(row_obj)

        label = ttk.Label(self.dropdown_frame, text=f"{row_number})", font=("Arial", 12, "bold"))
        label.grid(row=row, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
        row_obj["label"] = label

    def execute(self):
        print("Execution started.")
        self.stop_execution = False
        self.action_queue = [(0, None)]
        self.root.after(1000, self.process_queue)

    def process_queue(self):
        if self.action_queue:
            row_index, repeat_count = self.action_queue.pop(0)
            self._execute_step(row_index, repeat_count)
        else:
            self.stop_execution = True

    def hold_key(self, key, interval=50):
        if key in self.held_buttons:
            if key.isalnum():
                keyboard.write(key)
            else:
                keyboard.press(key)
                keyboard.release(key)
            self.root.after(interval, self.hold_key, key, interval)

    def _execute_step(self, row_index, repeat_count=None):
        print(f"Executing row {row_index} (repeat count: {repeat_count})")
        if not self.stop_execution:
            row = self.rows[row_index]
            main_dropdown = row["main_dropdown"]

            main_value = row["main_var"].get()
            extra_values = []

            for widget in row["extra_widgets"]:
                if isinstance(widget, ttk.Entry):
                    extra_values.append(widget.get())
                elif isinstance(widget, ttk.OptionMenu):
                    text = widget["text"]
                    if text in ['Up', 'Down']:
                        extra_values.append(text)

            if main_value == 'Click':
                print(f"Clicking {extra_values[0]}")
                self.click('Down')
                self.click('Up')

            if main_value == 'Press':
                key = extra_values[0]
                action = extra_values[1]  # Get the Press/Hold/Release action from the dropdown1
                if action == 'Hold':
                    print(f"Holding {key}")
                    self.held_buttons.add(key)
                    self.hold_key(key)
                elif action == 'Release':
                    print(f"Releasing {key}")
                    keyboard.release(key)
                    self.held_buttons.discard(key)
                else:  # action is 'Press'
                    print(f"Pressing {key}")
                    if key.isalnum():
                        keyboard.write(key)
                    else:
                        keyboard.press(key)
                        keyboard.release(key)

            elif main_value == 'Wait':
                print(f"Waiting {extra_values[0]} seconds")
                self.root.after(int(float(extra_values[0]) * 1000), self._execute_step, row_index + 1, repeat_count)
                return

            elif main_value == 'Return':
                if self.last_key is not None:
                    print(f"Returning to step {extra_values[0]}")
                    self.press(self.last_key, 'Up')

                return_row = self.rows[int(extra_values[0]) - 1]

                if len(extra_values) > 1 and extra_values[1]:
                    repeat_count = int(extra_values[1]) if repeat_count is None else repeat_count
                else:
                    repeat_count = -1

                if repeat_count != 0:
                    repeat_count -= 1
                    self.root.after(1, self._execute_step, self.rows.index(return_row), repeat_count)
                    return

            if row_index + 1 < len(self.rows):
                self.root.after(1, self._execute_step, row_index + 1, repeat_count)
            else:
                self.root.after(1, self.process_queue)

root = ThemedTk(theme="equilux")  # Use ThemedTk with the Equilux theme
app = App(root)
root.mainloop()
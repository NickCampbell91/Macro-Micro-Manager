import json
from tkinter import filedialog
import tkinter as tk
import tkinter.ttk as ttk

class FileManager:
    @staticmethod
    def save_to_file(rows):
        data = []
        for row in rows:
            main_value = row["main_var"].get()
            extra_values = []

            for widget in row["extra_widgets"]:
                if isinstance(widget, ttk.Entry):
                    extra_values.append(widget.get())
                elif isinstance(widget, ttk.OptionMenu):
                    text = widget.cget("text")
                    if text in ['Up', 'Down', 'Press', 'Hold', 'Release']:
                        extra_values.append(text)

            data.append([main_value] + extra_values)

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def load_from_file(app):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return None

        with open(file_path, 'r') as file:
            data = json.load(file)

        if data is None:
            return

        app.reset_rows()
        for index, row_data in enumerate(data):
            main_value = row_data[0]
            extra_values = row_data[1:]

            if index != 0:
                app.add_row()

            row = app.rows[-1]
            row["main_var"].set(main_value)

            value_index = 0
            for widget in row["extra_widgets"]:
                if isinstance(widget, ttk.Entry):
                    if value_index < len(extra_values):
                        widget.insert(0, extra_values[value_index])
                        value_index += 1
                elif isinstance(widget, ttk.OptionMenu):
                    if value_index < len(extra_values):
                        widget.children["textvariable"].set(extra_values[value_index])
                        value_index += 1
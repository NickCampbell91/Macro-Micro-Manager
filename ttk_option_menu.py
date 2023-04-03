from tkinter import ttk

class TTKOptionMenu(ttk.Combobox):
    def __init__(self, parent, variable, *values, **kwargs):
        self.variable = variable
        super().__init__(parent, textvariable=self.variable, values=values, width=8, **kwargs)
        self.variable.set(values[0]) if values else None
        self.configure(state="readonly")
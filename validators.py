class Validator:
    @staticmethod
    def validate_float(input_str):
        if input_str == '':
            return True
        try:
            float(input_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_integer_range(input_str, rows):
        if input_str == '':
            return True
        try:
            value = int(input_str)
            return 0 <= value < len(rows)
        except ValueError:
            return False

    @staticmethod
    def validate_non_negative_integer(input_str):
        if input_str == '':
            return True
        try:
            value = int(input_str)
            return value >= 0
        except ValueError:
            return False
        
    @staticmethod
    def get_special_key_map():
        return {
            'enter': 'enter',
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right',
            'backspace': 'backspace',
            'tab': 'tab',
            'capslock': 'caps_lock',
            'shift': 'shift',
            'ctrl': 'control',
            'alt': 'alt',
            'space': 'space',
            'esc': 'escape',
            'insert': 'insert',
            'delete': 'delete',
            'home': 'home',
            'end': 'end',
            'pageup': 'page_up',
            'pagedown': 'page_down',
            'numlock': 'num_lock',
            'scrolllock': 'scroll_lock',
            'printscreen': 'print_screen',
            'pause': 'pause',
            'f1': 'f1',
            'f2': 'f2',
            'f3': 'f3',
            'f4': 'f4',
            'f5': 'f5',
            'f6': 'f6',
            'f7': 'f7',
            'f8': 'f8',
            'f9': 'f9',
            'f10': 'f10',
            'f11': 'f11',
            'f12': 'f12',
        }

    @staticmethod
    def validate_key_input(key_input, special_key_map):
        special_key_map = Validator.get_special_key_map()
        if len(key_input) == 1:
            return True
        elif key_input.lower() in special_key_map:
            return True
        else:
            return False

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

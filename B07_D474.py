#B17_D474.py
# Bot Data Manager

class D474:
    def __init__(self):
        self._flashdata = None

    def set(self, data):
        color_on = "\033[31m"
        color_off = "\033[0m"
        self._flashdata = color_on + data + color_off

    def get_and_reset(self):
        data = self._flashdata if self._flashdata is not None else ""
        self._flashdata = None
        return data

    # # ANSI escape codes for the primary (basic) colors:
    # Black: \033[30m
    # Red: \033[31m
    # Green: \033[32m
    # Yellow: \033[33m
    # Blue: \033[34m
    # Magenta: \033[35m
    # Cyan: \033[36m
    # White: \033[37m

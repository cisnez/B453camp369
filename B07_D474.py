#B07_D474.py
# Bot as Data Manager
import logging

logging.basicConfig(filename='z.log', 
                    filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

class D474:
    """
    This class represents a Data Manager, providing logging functionalities. 
    It is capable of logging data with different severity levels, both to console (with color) and to a log file.
    
    Attributes:
        _flashdata: A private attribute used by all other modules for passing ALL flagged messages to the console and only log to file based on the level set in `logging.basicConfig`.
        level_colors: A mapping from log levels to their corresponding console display colors.
        level_mapping: A mapping from log levels to their corresponding logging functions.
    """

    def __init__(self):
        """
        Initializes a D474 instance.
        """
        self._flashdata = None
        self.level_colors = {
            "debug": "\033[32m",  # Green
            "info": "\033[36m",  # Cyan
            "warning": "\033[33m",  # Yellow
            "error": "\033[31m",  # Red
            "critical": "\033[35m",  # Magenta
        }
        self.level_mapping = {
            "debug": logging.debug,
            "info": logging.info,
            "warning": logging.warning,
            "error": logging.error,
            "critical": logging.critical,
        }

    def set_flash(self, level, data):
        """
        Logs data at a certain level, both to the console (with color) and to a log file (without color).
        
        Args:
            level (str): The log level, can be 'debug', 'info', 'warning', 'error', or 'critical'.
            data (str): The data to be logged.
        """
        color = self.level_colors.get(level.lower(), "\033[37m") # Default to white if level is not recognized
        new_message = color + level.upper() + ': ' + data + "\033[0m"
        
        # Append new message with a newline if flashdata already exists, otherwise just set the new message
        self._flashdata = self._flashdata + '\n' + new_message if self._flashdata else new_message

        # Also log the data with appropriate level
        log_func = self.level_mapping.get(level.lower(), logging.info)  # Default to logging.info if level is not recognized
        log_func(data)

    def get_flash_and_reset(self):
        """
        Retrieves the current log messages and clears them.
        
        Returns:
            data (str): The current log messages.
        """
        data = self._flashdata if self._flashdata is not None else ""
        self._flashdata = None
        return data

# In this version:

# 1. The `set_flash` method logs data in color for the console output and writes logging data to a file (without color). The color and file logging activity are determined by the provided level.

# 2. The `get_flash_and_reset` method retrieves and clears any buffer of flash data.

# 3. To make the class D474 display different log levels with corresponding colors for the console user, we define a dictionary to map each level to its color code, then use this mapping when setting `_flashdata`. 

#     ANSI escape codes for the primary (basic) colors:
#       - Black: \033[30m
#       - Red: \033[31m
#       - Green: \033[32m
#       - Yellow: \033[33m
#       - Blue: \033[34m
#       - Magenta: \033[35m
#       - Cyan: \033[36m
#       - White: \033[37m

# 4.  In your case, your D474 class isn't managing any such resources directly, so there's no need to close it.

#       In Python, you can use the with statement for automatic resource management. Classes that support this define a method named __enter__ that is called when the instance is created in a with statement, and a method named __exit__ that is called when the with block is exited. This __exit__ method usually takes care of any necessary cleanup. If your D474 class needed to clean up any resources, you would define these methods and use it with a with statement.

#       If you ever expand your D474 class to manage such resources, then you should provide a way to close them, either by defining __enter__ and __exit__ methods and using with, or by defining a close or cleanup method that needs to be called explicitly when you're done with the D474 instance.
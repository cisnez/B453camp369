#B07_D474.py
# Bot Data Manager
import logging
import yaml

logging.basicConfig(filename='z.log', 
                    filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class D474:
    def __init__(self):
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
        color = self.level_colors.get(level.lower(), "\033[37m")  # Default to white if level is not recognized
        new_message = color + level.upper() + ': ' + data + "\033[0m"
        
        # Append new message with a newline if flashdata already exists, otherwise just set the new message
        self._flashdata = self._flashdata + '\n' + new_message if self._flashdata else new_message

        # Also log the data with appropriate level
        log_func = self.level_mapping.get(level.lower(), logging.info)  # Default to logging.info if level is not recognized
        log_func(data)

    def get_flash_and_reset(self):
        data = self._flashdata if self._flashdata is not None else ""
        self._flashdata = None
        return data

    @staticmethod
    def merge_yaml_files(file_paths):
        merged_data = {}
        for file_path in file_paths:
            with open(file_path, "r", encoding='utf-8') as f:
                data = yaml.safe_load(f)
                for key, value in data.items():
                    if value is None:  # If the value is None, do nothing.
                        pass
                    elif isinstance(value, list):
                        if key not in merged_data or merged_data[key] is None:
                            merged_data[key] = value
                        else:
                            merged_data[key] += value
                    elif isinstance(value, dict):
                        if key not in merged_data or merged_data[key] is None:
                            merged_data[key] = value
                        else:
                            merged_data[key].update(value)
                    else:  # If the value is not None, list, or dict, replace the existing value.
                        merged_data[key] = value
        return merged_data

    @staticmethod
    def load_yaml_file(filename):
        try:
            with open(filename, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"The file {filename} was not found.")
        except yaml.YAMLError as e:
            logging.error(f"Error parsing the file {filename}: {str(e)}")

# In this version:

# 1. A `level_mapping` dictionary maps string levels to corresponding functions from the `logging` module.

# 2. The `set_flash` method now also logs the data with the level specified by the caller. If the caller provides a level that isn't recognized, it defaults to `logging.info`.

# 3. The `get_flash_and_reset` method logs a debug-level message indicating that the flash data is being retrieved and reset.

# 4. To make the class D474 handle different log levels with corresponding colors, you can define a dictionary to map each level to its color code, then use this mapping when setting _flashdata. Here's how you could do it:
  # # ANSI escape codes for the primary (basic) colors:
    # Black: \033[30m
    # Red: \033[31m
    # Green: \033[32m
    # Yellow: \033[33m
    # Blue: \033[34m
    # Magenta: \033[35m
    # Cyan: \033[36m
    # White: \033[37m

# 5. Say something about the YAML functionality
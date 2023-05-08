#B17_D474.py
import os

class D474:
    def __init__(self, path="/source/_img_/", filename=None, file_type="jpg"):
        self.path = path
        self.filename = filename if filename is not None else self.generate_random_string()
        self.file_type = file_type

    @staticmethod
    def generate_random_string():
        # Get the current timestamp as a string
        timestamp = str(time.time())
        
        # Create a SHA-256 hash object
        hasher = hashlib.sha256()
        
        # Update the hash object with the timestamp
        hasher.update(timestamp.encode('utf-8'))
        
        # Get the hexadecimal representation of the hash
        random_string = hasher.hexdigest()
        
        return random_string

    def save_image(self, image):
        img_path = os.path.join(self.path, f"{self.filename}.{self.file_type}")
        image.save(img_path)
        return img_path

    def save_details(self, prompt, seed, guidance_scale, steps):
        txt_path = os.path.join(self.path, f"{self.filename}.txt")
        with open(txt_path, 'w') as f:
            f.write(f"Seed: {seed}\n")
            f.write(f"Guidance Scale: {guidance_scale}\n")
            f.write(f"Steps: {steps}\n")
            f.write(f"Prompt: {prompt}\n")
        return txt_path

class D474FL45H:
    def __init__(self):
        self._flashdata = None

    def set(self, data):
        color_on = "\033[31m"
        color_off = "\033[0m"
        self._flashdata = color_on + data + color_off
        # # ANSI escape codes for the primary (basic) colors:
        # Black: \033[30m
        # Red: \033[31m
        # Green: \033[32m
        # Yellow: \033[33m
        # Blue: \033[34m
        # Magenta: \033[35m
        # Cyan: \033[36m
        # White: \033[37m

    def get_and_reset(self):
        data = self._flashdata
        self._flashdata = None
        return data

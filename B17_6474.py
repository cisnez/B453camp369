#B17_D474.py
import os
import hashlib
import time

class D474:
    def __init__(self, path="/source/_img_/", filename=None, file_type="jpg", aws_helper=None):
        self.path = path
        self.filename = filename if filename is not None else self.timestamp2sha256()
        self.file_type = file_type
        self.aws_helper = aws_helper

    @staticmethod
    def timestamp2sha256():
        # Get the current timestamp as a string
        timestamp = str(time.time())
        
        # Create a SHA-256 hash object
        hasher = hashlib.sha256()
        
        # Update the hash object with the timestamp
        hasher.update(timestamp.encode('utf-8'))
        
        # Get the hexadecimal representation of the hash
        sha256_string = hasher.hexdigest()
        
        return sha256_string

    def save_image(self, image, s3_bucket=None, s3_key=None):
        img_path = os.path.join(self.path, f"{self.filename}.{self.file_type}")
        image.save(img_path)

        if self.aws_helper and s3_bucket and s3_key:
            self.aws_helper.save_to_s3(img_path, s3_bucket, s3_key)

        return img_path

    def save_details(self, prompt, seed, guidance_scale, steps, s3_bucket=None, s3_key=None):
        txt_path = os.path.join(self.path, f"{self.filename}.txt")
        with open(txt_path, 'w') as f:
            f.write(f"Seed: {seed}\n")
            f.write(f"Guidance Scale: {guidance_scale}\n")
            f.write(f"Steps: {steps}\n")
            f.write(f"Prompt: {prompt}\n")

        if self.aws_helper and s3_bucket and s3_key:
            self.aws_helper.save_to_s3(txt_path, s3_bucket, s3_key)

        return txt_path

    def get_full_filename(self, file_type=None):
        if file_type is None:
            file_type = self.file_type
        return os.path.join(self.path, f"{self.filename}.{file_type}")

class D474FL45H:
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

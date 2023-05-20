#B17_D474.py
import os
import hashlib
import time
from pathlib import Path

class D474:
    def __init__(self, path="/source/_img_/", filename=None, file_type="jpg", aws_helper=None):
        self.path = path
        self.filename = filename if filename is not None else self.timestamp2sha256()
        self.file_type = file_type
        self.aws_helper = aws_helper
        self._flashdata = None

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
            self.aws_helper.write_s3(img_path, s3_bucket, s3_key)

        return img_path

    def save_details(self, prompt, seed, guidance_scale, steps, s3_bucket=None, s3_key=None):
        txt_path = os.path.join(self.path, f"{self.filename}.txt")
        with open(txt_path, 'w') as f:
            f.write(f"Seed: {seed}\n")
            f.write(f"Guidance Scale: {guidance_scale}\n")
            f.write(f"Steps: {steps}\n")
            f.write(f"Prompt: {prompt}\n")

        if self.aws_helper and s3_bucket and s3_key:
            self.aws_helper.write_s3(txt_path, s3_bucket, s3_key)

        return txt_path
        
    async def move_files_to_s3(self, bot):
        # Specify the source and target directories
        src_dir = Path(bot.local_bucket_path + "/_img_/2023")
        target_dir = "_img_/2023"

        # For each day in the year
        for month in range(1, 13):
            for day in range(1, 32):

                # Build the path to the daily folder
                daily_folder = src_dir / f"{month:02d}" / f"{day:02d}"

                # If the daily folder exists
                if daily_folder.exists():

                    # For each .jpg file in the daily folder
                    for jpg_file in daily_folder.glob("*.jpg"):

                        # Make sure there's a corresponding .txt file
                        txt_file = jpg_file.with_suffix('.txt')
                        if txt_file.exists():

                            # Rename the files based on the hash of the .jpg file's creation time
                            new_filename = D474.timestamp2sha256(jpg_file.stat().st_ctime)
                            jpg_file.rename(jpg_file.with_name(new_filename))
                            txt_file.rename(txt_file.with_name(new_filename))

                            # Define the target paths
                            s3_key_jpg = f"{target_dir}/{month:02d}/{day:02d}/{new_filename}.jpg"
                            s3_key_txt = f"{target_dir}/{month:02d}/{day:02d}/{new_filename}.txt"

                            # Move the files to S3
                            bot.aws_bit.write_s3(str(jpg_file), bot.aws_bucket_path, s3_key_jpg)
                            bot.aws_bit.write_s3(str(txt_file), bot.aws_bucket_path, s3_key_txt)

    def get_full_filename(self, file_type=None):
        if file_type is None:
            file_type = self.file_type
        return os.path.join(self.path, f"{self.filename}.{file_type}")

#B17_AW5.py
# (was B17_4W5.py , ren respects first letter of platform)
import boto3
import logging
from botocore.exceptions import NoCredentialsError, BotoCoreError

class AW5:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region="us-west-1"):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

        try:
            self.s3 = boto3.client(
                "s3",
                region_name=self.aws_region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )
        except BotoCoreError as e:
            logging.error(f"Failed to connect to AWS: {e}")
            raise e

    def upload_file_to_s3(self, file_path, bucket_name, s3_key):
        try:
            with open(file_path, "rb") as data:
                self.s3.upload_fileobj(data, bucket_name, s3_key)
            logging.info(f"File uploaded to {bucket_name}/{s3_key}")
        except FileNotFoundError:
            logging.error("The file was not found.")
            raise
        except NoCredentialsError:
            logging.error("Credentials not available")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise e

    def download_file_from_s3(self, bucket_name, s3_key, file_path):
        try:
            with open(file_path, "wb") as file:
                self.s3.download_fileobj(bucket_name, s3_key, file)
            logging.info(f"File downloaded from {bucket_name}/{s3_key}")
        except FileNotFoundError:
            logging.error("The file was not found.")
            raise
        except NoCredentialsError:
            logging.error("Credentials not available")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise e

# Here's the complete example of creating an instance of B17_4W5 with the required AWS credentials and passing it to the D474 class when needed:

# --- python code ---
# aws_helper = B17_4W5(
#     aws_access_key_id="your_aws_access_key_id",
#     aws_secret_access_key="your_aws_secret_access_key",
#     aws_region="your_aws_region",
# )

# d474 = D474(
#     path="your/local/path",
#     filename="your_filename",
#     file_type="jpg",
#     aws_helper=aws_helper
# )

# # When saving an image or details, you can now pass the S3 bucket and S3 key to save the file to S3
# image = ... # Your image object
# s3_bucket = "your-s3-bucket-name"
# s3_key = "your/s3/key.jpg"

# d474.save_image(image, s3_bucket=s3_bucket, s3_key=s3_key)

# prompt = "your_prompt"
# seed = 123
# guidance_scale = 0.5
# steps = 10
# s3_key = "your/s3/key.txt"

# d474.save_details(prompt, seed, guidance_scale, steps, s3_bucket=s3_bucket, s3_key=s3_key)
# This approach allows you to use the D474 class without AWS credentials when they are not needed. If you want to save files to an S3 bucket, you can create an instance of B17_4W5 with the required credentials and pass it to the D474 class.

# I apologize for the confusion. I misunderstood your requirements and provided a solution that doesn't work with Discord. Unfortunately, there is no direct method to hide the text file preview while sending it as an attachment in Discord.

# However, there's a workaround that we can use. Instead of sending the text file as an attachment, we can store the text file on a server or a cloud service like AWS S3, and provide a link to the text file. The link to the text file can then be included in the embed message.

# Here's an example of how to achieve this using an AWS S3 bucket:

# 1. First, you need to set up an AWS S3 bucket and configure the required permissions. You can follow this guide: https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html

# 2. Install the AWS SDK for Python (Boto3) by running:

# ```bash
# pip install boto3
# ```

# 3. Configure your AWS credentials by following this guide: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration

# 4. Modify your code to upload the text file to the S3 bucket and generate a link:

# ```python
# import boto3

# class D15B17:
#     # ... existing methods ...

#     def upload_to_s3(self, local_path, s3_key):
#         s3 = boto3.client('s3')
#         bucket_name = 'your-bucket-name'  # Replace with your bucket name
#         s3.upload_file(local_path, bucket_name, s3_key)
#         return f'https://{bucket_name}.s3.amazonaws.com/{s3_key}'

# # ... rest of the code ...

# elif message.content.startswith('.art'):
#     # ... existing code ...

#     try:
#         seed, guidance_scale, steps, full_prompt, image_path, txt_path = self.txt2img_bit.generate_image(full_prompt)
#         print(f'generate_image returned\ntxt_path: {txt_path}')
#     except Exception as e:
#         content = f"Error generating image: {e}"
#         await message.channel.send(content=content)
#         print(content)
#         return

#     try:
#         d474_image = D474(path=self.txt2img_bit.path, filename=self.txt2img_bit.filename, file_type="jpg")
#         d474_txt = D474(path=self.txt2img_bit.path, filename=self.txt2img_bit.filename, file_type="txt")

#         with open(image_path, "rb") as img_file:
#             content = "Art is the expression of the soul!"
#             image_file = discord.File(img_file, d474_image.get_full_filename())

#             # Upload the text file to S3 and generate a link
#             txt_s3_link = self.upload_to_s3(txt_path, d474_txt.get_full_filename())

#             # Create an embed with the image, title, and a link to the text file
#             embed = discord.Embed(title=content, description=f'[Download text file]({txt_s3_link})')
#             embed.set_image(url=f"attachment://{d474_image.get_full_filename()}")

#             # Send the embed and image file
#             await message.channel.send(embed=embed, files=[image_file])
#     except Exception as e:
#         content = f"Error generating image: {e}"
#         await message.channel.send(content=content)
#         print(content)
#         return
# ```

# This code will upload the text file to an S3 bucket and provide a link to the text file in the embed message. Users can click the link to download the text file without it being shown as a preview in the message. Remember to replace `'your-bucket-name'` with the name of your S3 bucket.
#B17_AW5.py
import boto3
from botocore.exceptions import NoCredentialsError, BotoCoreError
from pathlib import Path

class AW5:
    def __init__(self, secrets, data, aws_access_key_id, aws_secret_access_key, aws_region):
        self.secrets = secrets
        self.data = data
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
            self.data.set_flash('debug', f"AW5 constructor trying `self.s3 = boto3.client()`")
        except BotoCoreError as e:
            self.data.set_flash('error', f"Failed to connect to AWS: {e}")
            raise e

    def write_s3(self, bucket_name, s3_key, data):
        try:
            self.data.set_flash('debug', f"write_s3: [bucket_name: {bucket_name}, s3_key: {s3_key}, data: {data}")
            self.s3.put_object(Body=data, Bucket=bucket_name, Key=s3_key)
            self.data.set_flash('info', f"File uploaded to {bucket_name}/{s3_key}")
        except NoCredentialsError:
            self.data.set_flash('error', "Credentials not available")
            raise
        except Exception as e:
            self.data.set_flash('error', f"write_s3 error occurred: {e}")
            raise e

    def read_s3(self, bucket_name, s3_key):
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=s3_key)
            data = response['Body'].read()
            self.data.set_flash('info', f"File downloaded from {bucket_name}/{s3_key}")
            return data
        except NoCredentialsError:
            self.data.set_flash('error', "Credentials not available")
            raise
        except Exception as e:
            self.data.set_flash('error', f"read_s3 error occurred: {e}")
            raise e

    def delete_s3(self, bucket_name, s3_key):
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=s3_key)
            self.data.set_flash('info', f"File deleted from {bucket_name}/{s3_key}")
        except NoCredentialsError:
            self.data.set_flash('error', "Credentials not available")
            raise
        except self.s3.exceptions.NoSuchKey:
            self.data.set_flash('warning', f"Object {s3_key} does not exist in {bucket_name}")
        except Exception as e:
            self.data.set_flash('error', f"An error occurred during object deletion: {e}")
            raise e

    async def test_s3(self, test_bucket, test_key, test_content):
        try:
            self.data.set_flash('debug', f"S3 test: [test_bucket: {test_bucket}, test_key: {test_key}, test_content: {test_content}")

            # Write the encrypted file
            encrypted_test_content = self.secrets.encrypt_data(test_content)
            self.data.set_flash('debug', f"S3 test: encrypted_test_content = {encrypted_test_content}")
            self.write_s3(test_bucket, test_key, encrypted_test_content)

            # Read the file back and decrypt it
            read_content_bytes = self.read_s3(test_bucket, test_key)
            decrypted_read_content = self.secrets.decrypt_data(read_content_bytes)
            self.data.set_flash('debug', f"S3 test: decrypted_read_content = {decrypted_read_content}")

            # Check if decrypted_read_content matches test_content
            if decrypted_read_content != test_content:
                self.data.set_flash('debug', f"S3 test: decrypted_read_content != test_content")
                return False  # Something went wrong
            else:
                self.data.set_flash('debug', f"S3 test: decrypted_read_content == test_content")

            # If the write and read both worked, delete the test file
            try:
                self.delete_s3(test_bucket, test_key)
                self.data.set_flash('debug', f"delete_s3 test passed for {test_bucket}/{test_key}")
            except NoCredentialsError:
                self.data.set_flash('error', "Credentials not available")
                return False
            except self.s3.exceptions.NoSuchKey:
                self.data.set_flash('warning', f"Object {test_key} does not exist in {test_bucket}")
            except Exception as e:
                self.data.set_flash('error', f"An error occurred during S3 test: {e}")
                return False
        except Exception as e:
            self.data.set_flash('error', f"An error occurred during S3 test: {e}")
            return False
        return True

# It appears you're trying to use `self.s3_client` and `self.move_files_to_s3` from the `B17` class, but these attributes and methods aren't defined in that class. 

# Here's how you can address the issues:

# 1. If `s3_client` is a part of `AW5` class, you should use it like this:
# ```python
# self.aws_bit.s3_client
# ```
# So, the `test_s3` method in `B17` class should be like this:
# ```python
#     async def test_s3(self):
#         test_filename = "test_file.txt"
#         test_content = "This is a test."
        
#         # Write the file
#         self.aws_bit.s3_client.put_object(Body=test_content, Bucket=self.storage_path, Key=test_filename)

#         # Read the file back
#         s3_object = self.aws_bit.s3_client.get_object(Bucket=self.storage_path, Key=test_filename)
#         file_content = s3_object["Body"].read().decode()

#         if file_content == test_content:
#             return True  # The write and read both worked
#         else:
#             return False  # Something went wrong
# ```
# 2. Regarding `self.move_files_to_s3`, you have not implemented this method in the `B17` class. You should define this method in the `B17` class similar to `test_s3` method if you want to use it. The implementation of this method depends on how you want to move files to S3. Generally, you could use `put_object` or `upload_file` functions of `s3_client` to upload a file to S3.

# Here's an example of how you might implement `move_files_to_s3`:

# ```python
#     async def move_files_to_s3(self):
#         # assuming you have a list of files to upload
#         files_to_upload = ["file1.txt", "file2.txt"]

#         for filename in files_to_upload:
#             with open(filename, "rb") as data:
#                 self.aws_bit.s3_client.put_object(Body=data, Bucket=self.storage_path, Key=filename)
# ```

# In this example, we're uploading files listed in `files_to_upload` from your local system to S3. Replace `files_to_upload` with the actual list of files you want to upload.

# Please note that error handling is not included in these code snippets, so you might want to add appropriate error handling depending on your needs.
#B17_AW5.py
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

    def write_s3(self, path, filename, data):
        try:
            bucket_name, s3_key = self._get_bucket_and_key(path, filename)
            self.s3.put_object(Body=data, Bucket=bucket_name, Key=s3_key)
            logging.info(f"File uploaded to {bucket_name}/{s3_key}")
        except NoCredentialsError:
            logging.error("Credentials not available")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise e

    def read_s3(self, path, filename):
        try:
            bucket_name, s3_key = self._get_bucket_and_key(path, filename)
            response = self.s3.get_object(Bucket=bucket_name, Key=s3_key)
            data = response['Body'].read()
            logging.info(f"File downloaded from {bucket_name}/{s3_key}")
            return data
        except NoCredentialsError:
            logging.error("Credentials not available")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise e

    def delete_s3(self, path, filename):
        try:
            bucket_name, s3_key = self._get_bucket_and_key(path, filename)
            self.s3.delete_object(Bucket=bucket_name, Key=s3_key)
            logging.info(f"File deleted from {bucket_name}/{s3_key}")
        except NoCredentialsError:
            logging.error("Credentials not available")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise e

    def _get_bucket_and_key(self, path, filename):
        # Here I'm assuming that the path format is /bucketname/keypath
        bucket_name = path.parts[1]
        key_parts = list(path.parts[2:]) + [filename]
        s3_key = "/".join(key_parts)
        return bucket_name, s3_key

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
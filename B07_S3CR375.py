#B07_S3CR375.py
# Bot as Secrets Manager
from cryptography.fernet import Fernet
import hashlib
import time
import yaml
import os

class S3CR375:
    def __init__(self, data, key_file: str = None):
        self.data = data
        self.key_file = key_file or "key.key"  # use provided key_file or default to "key.key"
        
        if os.path.isfile(self.key_file):
            self.load_key()
            self.data.set_flash('debug', f"Constructing SecretsManager with `load_key`.")
        else:
            self.key = None
            self.cipher_suite = None
            self.data.set_flash('debug', f"Constructing SecretsManager with no key.")

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def save_key(self, key_file: str):
        with open(key_file, 'wb') as key_file:
            key_file.write(self.key)

    def load_key(self):
        with open(self.key_file, 'rb') as key_file:
            self.key = key_file.read()
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data):
        data_bytes = bytes(str(data), 'utf-8')
        return self.cipher_suite.encrypt(data_bytes)

    def decrypt_data(self, encrypted_data):
        decrypted_data_bytes = self.cipher_suite.decrypt(encrypted_data)
        decrypted_data_str = decrypted_data_bytes.decode('utf-8')
        return yaml.safe_load(decrypted_data_str)

    def save_encrypted_yaml(self, data, filename):
        encrypted_data = self.encrypt_data(data)
        with open(filename, 'wb') as f:
            f.write(encrypted_data)

    def load_encrypted_yaml(self, filename):
        try:
            with open(filename, 'rb') as f:
                encrypted_data = f.read()
        except FileNotFoundError:
            D474().set_flash('error', f"The file {filename} was not found.")
            return None
        return self.decrypt_data(encrypted_data)

    def timestamp2sha256(self):
        timestamp = str(time.time())
        hasher = hashlib.sha256()
        hasher.update(timestamp.encode('utf-8'))
        sha256_string = hasher.hexdigest()
        return sha256_string

## What's in this Version

# This version includes the following new features:

# 1. **Encrypted Data Handling**: The Secrets Manager now includes the methods `encrypt_data` and `decrypt_data`, which work directly with data rather than files. This makes it possible to encrypt/decrypt data in-memory without needing to write/read from files.

# 2. **Encrypted File Saving and Loading**: There are now methods `save_encrypted_yaml` and `load_encrypted_yaml`, which save/load encrypted data to/from a file. These methods handle the conversion between data and bytes, encryption/decryption, and file I/O, simplifying the use of encryption in file handling.

# 3. **Integration with DataManager (D474)**: The refactored Secrets Manager is designed to be easily integrated with the new DataManager (D474). In DataManager, when saving or loading data, use `secrets_manager.save_encrypted_yaml` or `secrets_manager.load_encrypted_yaml` instead of writing/reading from files directly. This ensures that the data is encrypted/decrypted as needed.

# 4. **SHA256 Timestamps**: The `timestamp2sha256` method generates a SHA256 hash of the current timestamp. This could be useful for creating unique identifiers or checking the integrity of timestamps.

# ## Usage with DataManager and start_bot method

# To use the Secrets Manager with DataManager in the `start_bot` method, follow these steps:

# 1. Initialize a secrets_manager with a key. If the key doesn't exist yet, use `generate_key` and `save_key` to create one.

# 2. Initialize DataManager with the instance of secrets_manager.

# 3. In the `start_bot` method, instead of retrieving keys and tokens directly from DataManager, use the `get_key` method from secrets_manager. The bot name and key name should be provided as arguments.

# Here's an example initialization in `start_bot` method:

# ```python
# class Signal369:
#     # ...

#     async def start_bot(self, bot_name: str):
#         secrets_manager = S3CR375('key.key')
#         data_manager = Signal369(secrets_manager)
        
#         try:
#             discord_token = data_manager.secrets_manager.get_key(bot_name, "discord_token")
#             aws_secret_access_key = data_manager.secrets_manager.get_key(bot_name, "aws_secret_access_key")
#             aws_access_key_id = data_manager.secrets_manager.get_key(bot_name, "aws_access_key_id")
#             openai_key = data_manager.secrets_manager.get_key(bot_name, "openai_api_key")
#             telegram_api_id = data_manager.secrets_manager.get_key(bot_name, "telegram_api_id")
#             telegram_api_hash = data_manager.secrets_manager.get_key(bot_name, "telegram_api_hash")

#             # ...rest of the start_bot method...
#         except Exception as e:
#             D474().set_flash('error', f"Failed to start bot due to: {str(e)}")
# ```

# Remember to modify the `get_key` method in SecretsManager and DataManager to suit your implementation. This is just a suggested way to organize your keys. It may not be the best way depending on your particular use case and requirements.
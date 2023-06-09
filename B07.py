# B07.py
import asyncio
from B07_B17 import B17

class B07:
    def __init__(self, loop, secrets, data, bot_name, bot_init_data, openai_api_key, discord_token, telegram_api_id, telegram_api_hash, aws_secret_access_key, aws_access_key_id):
        self.loop = loop
        self.secrets = secrets
        self.data = data
        self.bot_name = bot_name
        self.bot_init_data = bot_init_data
        self.leet_name = bot_init_data["7331eman"]
        # Set bot properties in dictionary
        self.properties = {
            "openai_api_key": openai_api_key,
            "discord_token": discord_token,
            "discord_id": self.bot_init_data["self_author_id"],
            "telegram_api_id": telegram_api_id,
            "telegram_api_hash": telegram_api_hash,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_access_key_id": aws_access_key_id,
        }
        self.bit_manager = None  # ensure self.bit_manager is always defined
        try:
            self.bit_manager = B17(self, self.loop, self.secrets, self.data, self.bot_name, self.bot_init_data, self._bit_switches(), self._bit_auth())
        except Exception as e:
            self.data.set_flash('critical', f"Bot failed to instantiate bit_manager: {str(e)}")

    async def start_bit_manager(self):
        pass
        retry_delay = 1  # or whatever initial delay you want
        while True:
            try:
                if self.bit_manager is not None:
                    await self.bit_manager.manage_bits()
                    # If we get here without an exception, reset the retry delay
                    retry_delay = 1
            except asyncio.CancelledError:
                # Log the cancellation
                self.data.set_flash('info', 'Bit manager was cancelled')
                return
            except Exception as e:
                self.data.set_flash('critical', f"Bit manager crashed: {str(e)}")
                # Increase the delay for each retry, to a maximum of (say) 60 seconds
                retry_delay = min(retry_delay * 2, 60)
                await asyncio.sleep(retry_delay)  # Wait before retrying

    def _bit_auth(self):
        return {
            "openai_api": {
                "api_key": self.properties["openai_api_key"]
            },
            "discord_api": {
                "bot_token": self.properties["discord_token"],
                "bot_id": self.properties["discord_id"]
            },
            "telegram_api": {
                "api_id": self.properties["telegram_api_id"],
                "api_hash": self.properties["telegram_api_hash"]
            },
            "aws_api": {
                "access_key_id": self.properties["aws_access_key_id"],
                "secret_access_key": self.properties["aws_secret_access_key"]
            },
            "txt2txt_api": {
                "api_key": None
            },
            "txt2img_api": {
                "api_key": None
            },
            "img2txt_api": {
                "api_key": None
            },
            "img2img_api": {
                "api_key": None
            }
        }

    def _bit_switches(self):
        return {
            "openai_api": self.properties["openai_api_key"] is not None,
            "discord_api": self.properties["discord_token"] is not None,
            "telegram_api": self.properties["telegram_api_id"] is not None and self.properties["telegram_api_hash"] is not None,
            "aws_api": self.properties["aws_access_key_id"] is not None and self.properties["aws_secret_access_key"] is not None,
            "txt2txt_api": False,
            "txt2img_api": None is not None,
            "img2txt_api": False,
            "img2img_api": None is not None
        }

    # _bit_switches checks if the bot has the necessary "ingredients" to initialize a bit, while get_bit_status checks if the bot has successfully used those "ingredients" to create a functioning bit.
    def get_bit_status(self):
        # Flash bit statuses
        bit_status = {
            "aws_api": self.bit_manager.aws_bit is not None,
            "discord_api": self.bit_manager.discord_bit is not None,
            "telegram_api": self.bit_manager.telegram_bit is not None,
            "openai_api": self.bit_manager.openai_bit is not None
        }
        self.data.set_flash('debug', f"Bit statuses for bot {self.bot_name}: {bit_status}")
        return bit_status

    def manage_bot(self):
        if self.bit_manager is not None:
            self.bit_manager.manage_bits()

    async def close(self):
        # Check if the bit_manager exists
        if self.bit_manager is not None:
            try:
                # Stop any active bits
                await self.bit_manager.stop_active_bits()

                # Clean up the resources related to bit_manager
                await self.bit_manager.cleanup()

                # Remove the bit_manager object
                self.bit_manager = None

                self.data.set_flash('info', f'Bot `{self.leet_name}` has been closed.')
            except Exception as e:
                self.data.set_flash('critical', f"Error closing bot `{self.leet_name}`: {str(e)}")
                raise e

# The Single Responsibility Principle (SRP), as part of SOLID principles, asserts that a class should have only one responsibility, or in other words, it should have only one reason to change. The intention is to make the software system easier to maintain and more robust against bugs.

# In your `B07` class, the responsibilities are well divided. Here's a summary of each responsibility and which method or set of methods fulfill it:

# 1. **Initialization and Configuration**: This responsibility involves setting up the object with the necessary data it needs to operate. In your `B07` class, the `__init__` and `_bit_switches` methods handle this responsibility. They set up the object's attributes and initialize the `bit_manager` with appropriate switches based on the provided initialization data.

# 2. **Bot Management**: This includes starting individual bits and managing them. The `start_bit` and `manage_bot` methods manage this responsibility. The `start_bit` method provides a way to individually start each bit, while `manage_bot` provides a mechanism to manage all the bits (presumably this includes checking their statuses and handling issues).

# 3. **Error Handling**: Error handling is a crucial responsibility in any system. It involves dealing with potential errors and exceptions that might occur during the execution of the program. In the `B07` class, this is handled by catching exceptions in various places and logging appropriate error messages, as seen in the `__init__`, `start_bit`, and `start` methods.

# 4. **Bot Execution**: The bot needs to continuously manage its bits, which is why there's a loop in the `start` method that keeps calling `manage_bits` method on the `bit_manager`. This responsibility is thus managed by the `start` method.

# While the `B07` class does have multiple methods that fulfill different responsibilities, it's important to note that the class as a whole adheres to the SRP. Its single responsibility could be defined as "Managing a bot and its bits," and every method in the class contributes to this overall responsibility in some way. This makes the `B07` class easier to maintain and understand. It also reduces the risk of bugs that could arise from having multiple responsibilities intertwined in the same class.
# B07.py
import logging
from B07_B17 import B17

class B07:
    def __init__(self, openai_api_key, discord_token, telegram_api_id, telegram_api_hash, aws_secret_access_key, bot_init_data):
        self.bot_init_data = bot_init_data

        # Prepare bot specific data
        self.openai_api_key = openai_api_key
        self.discord_token = discord_token
        self.telegram_api_id = telegram_api_id
        self.telegram_api_hash = telegram_api_hash
        self.aws_secret_access_key = aws_secret_access_key

        self.bot = None
        try:
            self.bot = B17(self.bot_config())
        except Exception as e:
            logging.error(f"Failed to instantiate bot: {str(e)}")

    def _bot_config(self):
        return {
            "openai_api_key": self.openai_api_key,
            "discord_token": self.discord_token,
            "telegram_api_id": self.telegram_api_id,
            "telegram_api_hash": self.telegram_api_hash,
            "aws_secret_access_key": self.aws_secret_access_key,
            "bot_init_data": self.bot_init_data
        }

    def manage_bot(self):
        if self.bot is not None:
            self.bot.manage_bits()

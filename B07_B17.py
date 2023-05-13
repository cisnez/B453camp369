#B07_B17.py
import openai
from discord.ext import commands       # pip install discord
from discord import Intents            # pip install discord
from B17_7X721M6 import TX721M6
from B17_D15C0RD import D15C0RD
from B17_T3L36R4M import T3L36R4M
from B17_M3554635 import M3554635
from B17_D474 import D474FL45H
from transformers import GPT2Tokenizer  # Import the tokenizer module

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Constants for `Wake Up` game.
ZIP = "219"
ZAP = "249"
ZOP = "209"

class B17(commands.Bot):
    def __init__(self, openai_api_key, discord_token, telegram_api_id, telegram_api_hash, bot_init_data):
        # Store bot init data in this object for other objects to use.
        self.bot_init_data = bot_init_data

        # Assign all yaml values within the _init_user.yaml file
        self.nicknames = bot_init_data["nicknames"]
        self.color = bot_init_data["color"]

        # Image dimensions for txt2img and img2img
        self.img_width = bot_init_data["img_width"]
        self.img_height = bot_init_data["img_height"]

        # Create an instance of the TX721M6 class for txt2img generation using the bot's properties
        self.txt2img_bit = TX721M6(txt2img_repo_id="danbrown/RPG-v4", img_width=self.img_width, img_height=self.img_height)

        # Initialize the OpenAI bit here
        self.openai_api_key = openai_api_key
        # Initialize the OpenAI bit here
        openai.api_key = openai_api_key
        
        # Create a message queue object
        self.message_queue = M3554635()

        # create a D474FL45H instance
        self.flash_data = D474FL45H()

        # Initialize the Discord bit here
        self.discord_token = discord_token
        self.discord_bot = D15C0RD(self, M3554635.Message)

        # Initialize the Telegram bit here
        self.telegram_bot = T3L36R4M(telegram_api_id, telegram_api_hash, self.message_queue, M3554635.Message, self.flash_data)

        # Parent class assignments for: super().__init__()
        intents = Intents(**bot_init_data["intents"])
        command_prefix = bot_init_data["command_prefix"]

        self.ignored_prefixes = bot_init_data["ignored_prefixes"]
        self.home_channel_id = bot_init_data["home_channel_id"]

        self.self_channel_id = bot_init_data["self_channel_id"]
        self.self_author_id = bot_init_data["self_author_id"]
        self.self_author_name = bot_init_data["self_author_name"]
        self.other_author_id = bot_init_data["other_author_id"]
        self.other_channel_id = bot_init_data["other_channel_id"]
        self.bot_channel_id = bot_init_data["bot_channel_id"]
        self.hello_channel_id = bot_init_data["hello_channel_id"]

        # Define Stable Diffusion model
        self.sd_model_id = bot_init_data["sd_model_id"]
        self.prePrompt = bot_init_data["prePrompt"]
        self.postPrompt = bot_init_data["postPrompt"]
        self.negPrompt = bot_init_data["negPrompt"]

        # # Replace nltk.word_tokenize() with GPT2Tokenizer.tokenize()
        self.prePrompt_tokens = tokenizer.tokenize(self.prePrompt)
        self.postPrompt_tokens = tokenizer.tokenize(self.postPrompt)
        self.negPrompt_tokens = tokenizer.tokenize(self.negPrompt)

        self.maxCLIPtokens = bot_init_data["maxCLIPtokens"]

        # A set ensures that these collections only store unique elements
        self.allow_author_ids = set(bot_init_data["allow_author_ids"])
        self.allow_channel_ids = set(bot_init_data["allow_channel_ids"])
        self.ignore_author_ids = set(bot_init_data["ignore_author_ids"])
        self.ignore_channel_ids = set(bot_init_data["ignore_channel_ids"])
        
        super().__init__(command_prefix=command_prefix, intents=intents)

        async def start(self, token):
            await self.run(token)
            # Send a ZIP message to start the handshake
            await self.discord_bot.message_queue.put(M3554635.Message(ZIP, "handshake"))

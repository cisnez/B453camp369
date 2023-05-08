#B07_B17.py
from discord.ext import commands       # pip install discord
from discord import Intents            # pip install discord
from B17_7X721M6 import TX721M6
from transformers import GPT2Tokenizer  # Import the tokenizer module

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

class B17(commands.Bot):
    def __init__(self, openai_api_key, discord_token, bot_init_data):
        self.openai_api_key = openai_api_key
        self.discord_token = discord_token

        # Assign all yaml values within the _init_user.yaml file
        self.nicknames = bot_init_data["nicknames"]
        self.color = bot_init_data["color"]

        # Image dimensions for txt2img and img2img
        self.img_width = bot_init_data["img_width"]
        self.img_height = bot_init_data["img_height"]

        # Create an instance of the TX721M6 class for txt2img generation using the bot's properties
        self.txt2img_bit = TX721M6(txt2img_repo_id="danbrown/RPG-v4", img_width=self.img_width, img_height=self.img_height)

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
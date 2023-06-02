# Old code
# from B17_TX721M6 import TX721M6
# from B17_M3554635 import M3554635
# from B17_T3L36R4M import T3L36R4M
# from B17_D15C0RD import D15C0RD
# from discord.ext import commands       # pip install discord
# from discord import Intents            # pip install discord
# import boto3
# from botocore.exceptions import NoCredentialsError
# from transformers import GPT2Tokenizer  # Import the tokenizer module
# import openai

# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# # Constants for `Wake Up` game.
# ZIP = "219"
# ZAP = "249"
# ZOP = "209"

#B07_B17.py
# Bit Manager
from B17_AW5 import AW5

class B17:
    def __init__(self, bot, loop, secrets, data, bot_name, bot_init_data, bit_switches, bit_auth):
        self.bot = bot
        self.loop = loop
        self.secrets = secrets
        self.data = data
        self.bot_name = bot_name
        self.bot_init_data = bot_init_data
        self.bit_switches = bit_switches
        self.bit_auth = bit_auth
        self.aws_bit = None
        self.discord_bit = None
        self.telegram_bit = None
        self.openai_bit = None
        self.data.set_flash('debug', f"{self.bot_name} constructed a new bit_manager. [bit_switches: {self.bit_switches}]")

    async def stop_active_bits(self):
        # Here you should implement the logic to stop any active bits
        self.data.set_flash('debug', f"Passing through `stop_active_bits`.")
        pass

    async def cleanup(self):
        # Here you should implement the logic to clean up any resources related to bits
        self.data.set_flash('debug', f"Passing through `cleanup`.")
        pass

    async def manage_bits(self):
        # Implement the functionality for managing bits.
        for bit, is_on in self.bit_switches.items():
            if is_on:
                # Depending on the bit, perform certain actions.
                if bit == 'aws_api':
                    await self.manage_aws()
                elif bit == 'discord_api':
                    await self.manage_discord()
                elif bit == 'openai_api':
                    await self.manage_openai()
                elif bit == 'telegram_api':
                    await self.manage_telegram()
                # Add more elif conditions for other bits.
        self.data.set_flash('debug', f"Passing through `manage_bits`.")

    async def manage_aws(self):
        if self.aws_bit is None:
            self._init_aws()
            self.data.set_flash('debug', f"Passing through `manage_aws`.")
            pass

    async def manage_discord(self):
        # Implement your Discord bot logic here.
        self.data.set_flash('debug', f"Passing through `manage_discord`.")
        pass

    async def manage_telegram(self):
        # Implement your Discord bot logic here.
        self.data.set_flash('debug', f"Passing through `manage_discord`.")
        pass

    async def manage_openai(self):
        # Implement your OpenAI logic here.
        self.data.set_flash('debug', f"Passing through `manage_openai`.")
        pass

    # You can add more manage_X methods for other bits.

    def init_bits(self):
        # Implement initialization for bits.
        # You might want to set initial states, load data, etc.
        for bit_name, is_on in self.bit_switches.items():
            if is_on:
                # Initialize all True bits.
                try:
                    if bit_name == 'discord_api':
                        self._init_discord()
                    elif bit_name == 'telegram_api':
                        self._init_aws()
                    elif bit_name == 'aws_api':
                        self._init_aws()
                    elif bit_name == 'openai_api':
                        self._init_openai()
                    self.data.set_flash('info', f"Initialized {bit_name} bit")
                except Exception as e:
                    self.data.set_flash('error', f"Failed to initialize {bit_name} bit: {str(e)}")

    def init_bit(self, bit_name):
        self.data.set_flash('debug', f"Entering init_bit with: {bit_name}")
        if bit_name in self.bit_switches:
            try:
                if bit_name == 'discord_api':
                    self._init_discord()
                elif bit_name == 'telegram_api':
                    self._init_telegram()
                elif bit_name == 'aws_api':
                    self.data.set_flash('debug', f"Passing through `aws_api`.")
                    self._init_aws()
                    self.data.set_flash('debug', f"Passed through `_init_aws` in `aws_api`.")
                elif bit_name == 'openai_api':
                    self._init_openai()
                self.data.set_flash('info', f"Initialized {bit_name} bit")
            except Exception as e:
                self.data.set_flash('error', f"Failed to initialize {bit_name} bit: {str(e)}")
        else:
            self.data.set_flash('warning', f"bit_name: {bit_name} not found in bit.bit_switches")

    def _init_discord(self):
        # Implement Discord initialization here.
        self.data.set_flash('debug', f"Passing through `_init_discord`.")
        pass

    def _init_telegram(self):
        # Implement Discord initialization here.
        self.data.set_flash('debug', f"Passing through `_init_telegram`.")
        pass

    def _init_aws(self):
        self.data.set_flash('debug', f"Entering `_init_aws` in `aws_api`.")
        try: 
            if 'aws_api' in self.bit_switches:
                aws_access_key_id = self.bot._bit_auth()['aws_api']['access_key_id']
                aws_secret_access_key = self.bot._bit_auth()['aws_api']['secret_access_key']
                try:
                    self.data.set_flash('debug', f"About to initialize AWS bit")
                    # Pass the bit_data instance to the AW5 class
                    aws_region = self.bot_init_data.get('aws_region')
                    self.data.set_flash('debug', f"AWS region: {aws_region}")
                    if aws_region:
                        self.aws_bit = AW5(self.secrets, self.data, aws_access_key_id, aws_secret_access_key, aws_region)
                    else:
                        self.data.set_flash('debug', f"AWS region is not configured for {self.bot_name}. Please check the _init_{self.bot_name}.yaml file.")

                    self.data.set_flash('info', f"Initialized AWS bit")
                except Exception as e:
                    self.data.set_flash('critical', f"Failed to initialize AWS bit: {str(e)}")
        except Exception as e:
            self.data.set_flash('critical', f"Unable to access bot._bit_auth method: {str(e)}")
        finally:
            self.data.set_flash('debug', f"Exiting `_init_aws` in `aws_api`.")

    def _init_openai(self):
        # Implement OpenAI initialization here.
        self.data.set_flash('debug', f"Passing through `_init_openai`.")
        pass

    # You can add more init_X methods for other bits.


    #     # Store bot init data in this object for other objects to use.
    #     self.bot_init_data = bot_init_data

    #     # Assign all yaml values within the _init_user.yaml file
    #     self.nicknames = bot_init_data["nicknames"]
    #     self.color = bot_init_data["color"]

        # Initialize the AWS bit here or local "bucket" if not initialized

    #     # Image dimensions for txt2img and img2img
    #     self.img_width = bot_init_data["img_width"]
    #     self.img_height = bot_init_data["img_height"]

    #     # Create an instance of the TX721M6 class for txt2img generation using the bot's properties
    #     self.txt2img_bit = TX721M6(txt2img_repo_id="danbrown/RPG-v4", img_width=self.img_width, img_height=self.img_height)

    #     # Initialize the OpenAI bit here
    #     self.openai_api_key = openai_api_key
    #     # Initialize the OpenAI bit here
    #     openai.api_key = openai_api_key
        
    #     # Create a message queue object
    #     self.message_queue = M3554635()


    #     # Initialize the Discord bit here
    #     self.discord_token = discord_token
    #     self.discord_bot = D15C0RD(self, M3554635.Message)

    #     # Initialize the Telegram bit here
    #     self.telegram_bot = T3L36R4M(telegram_api_id, telegram_api_hash, self.message_queue, M3554635.Message, self.flash_data)

    #     # Parent class assignments for: super().__init__()
    #     intents = Intents(**bot_init_data["intents"])
    #     command_prefix = bot_init_data["command_prefix"]

    #     self.ignored_prefixes = bot_init_data["ignored_prefixes"]
    #     self.home_channel_id = bot_init_data["home_channel_id"]

    #     self.self_channel_id = bot_init_data["self_channel_id"]
    #     self.self_author_id = bot_init_data["self_author_id"]
    #     self.self_author_name = bot_init_data["self_author_name"]
    #     self.other_author_id = bot_init_data["other_author_id"]
    #     self.other_channel_id = bot_init_data["other_channel_id"]
    #     self.bot_channel_id = bot_init_data["bot_channel_id"]
    #     self.hello_channel_id = bot_init_data["hello_channel_id"]

    #     # Define Stable Diffusion model
    #     self.sd_model_id = bot_init_data["sd_model_id"]
    #     self.prePrompt = bot_init_data["prePrompt"]
    #     self.postPrompt = bot_init_data["postPrompt"]
    #     self.negPrompt = bot_init_data["negPrompt"]

    #     # # Replace nltk.word_tokenize() with GPT2Tokenizer.tokenize()
    #     self.prePrompt_tokens = tokenizer.tokenize(self.prePrompt)
    #     self.postPrompt_tokens = tokenizer.tokenize(self.postPrompt)
    #     self.negPrompt_tokens = tokenizer.tokenize(self.negPrompt)

    #     self.maxCLIPtokens = bot_init_data["maxCLIPtokens"]

    #     # A set ensures that these collections only store unique elements
    #     self.allow_author_ids = set(bot_init_data["allow_author_ids"])
    #     self.allow_channel_ids = set(bot_init_data["allow_channel_ids"])
    #     self.ignore_author_ids = set(bot_init_data["ignore_author_ids"])
    #     self.ignore_channel_ids = set(bot_init_data["ignore_channel_ids"])
        
    #     super().__init__(command_prefix=command_prefix, intents=intents)
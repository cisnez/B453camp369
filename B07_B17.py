#B07_B17.py
# Bit Manager

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

from B17_D474 import D474
from B17_AW5 import AW5

class B17:
    def __init__(self, bot_name, bit_switches, bot_init_data, bot_data):
        self.bot_name = bot_name
        self.bit_switches = bit_switches
        self.bot_init_data = bot_init_data
        self.bot_data = bot_data
        self.bot_data.set_flash('debug', f"{self.bot_name} constructed a new bit_manager.")

    async def stop_active_bits(self):
        # Here you should implement the logic to stop any active bits
        self.bot_data.set_flash('debug', f"Passing through `stop_active_bits`.")
        pass

    async def cleanup(self):
        # Here you should implement the logic to clean up any resources related to bits
        self.bot_data.set_flash('debug', f"Passing through `cleanup`.")
        pass

    async def manage_bits(self):
        # Implement the functionality for managing bits.
        for bit, is_on in self.bit_switches.items():
            if is_on:
                # Depending on the bit, perform certain actions.
                if bit == 'discord_api':
                    await self.manage_discord()
                elif bit == 'openai_api':
                    await self.manage_openai()
                elif bit == 'discord_api':
                    await self.manage_discord()
                elif bit == 'openai_api':
                    await self.manage_openai()
                # Add more elif conditions for other bits.
        self.bot_data.set_flash('debug', f"Passing through `manage_bits`.")
    
    async def manage_aws(self):
        if self.aws_bit is not None:
            # Your AWS bit related management code goes here.
            self.bot_data.set_flash('debug', f"Passing through `manage_aws`.")
            pass

    async def manage_discord(self):
        # Implement your Discord bot logic here.
        self.bot_data.set_flash('debug', f"Passing through `manage_discord`.")
        pass

    async def manage_telegram(self):
        # Implement your Discord bot logic here.
        self.bot_data.set_flash('debug', f"Passing through `manage_discord`.")
        pass

    async def manage_openai(self):
        # Implement your OpenAI logic here.
        self.bot_data.set_flash('debug', f"Passing through `manage_openai`.")
        pass

    # You can add more manage_X methods for other bits.

    def init_bits(self):
        # Implement initialization for bits.
        # You might want to set initial states, load data, etc.
        for bit, is_on in self.bit_switches.items():
            if is_on:
                # Depending on the bit, initialize certain resources.
                if bit == 'aws_api':
                    self.init_aws()
                elif bit == 'discord_api':
                    self.init_discord()
                elif bit == 'openai_api':
                    self.init_openai()
                # Add more elif conditions for other bits.

    def init_aws(self):
        if 'aws_api' in self.bit_switches:
            aws_secret_access_key = self.bit_switches['aws_api']
            try:
                self.aws_bit = AW5(aws_secret_access_key)
                self.bot_data.set_flash('info', f"Initialized AWS bit")
            except Exception as e:
                self.bot_data.set_flash('error', f"Failed to initialize AWS bit: {str(e)}")

    def init_discord(self):
        # Implement Discord initialization here.
        self.bot_data.set_flash('debug', f"Passing through `init_discord`.")
        pass

    def init_openai(self):
        # Implement OpenAI initialization here.
        self.bot_data.set_flash('debug', f"Passing through `init_openai`.")
        pass

    async def test_s3(self):
        test_filename = "test_file.txt"
        test_content = "This is a test."
        
        # Write the file
        self.aws_bit.s3.put_object(Body=test_content, Bucket=self.storage_path, Key=test_filename)

        # Read the file back
        s3_object = self.aws_bit.s3.get_object(Bucket=self.storage_path, Key=test_filename)
        file_content = s3_object["Body"].read().decode()

        if file_content == test_content:
            self.bot_data.set_flash('info', "The write and read both worked")
            return True  # The write and read both worked
        else:
            self.bot_data.set_flash('error', "Something went wrong")
            return False  # Something went wrong

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
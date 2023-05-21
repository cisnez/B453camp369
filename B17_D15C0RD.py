#B17_D15C0RD.py
import discord
from discord.ext import commands
import asyncio
from queue import Queue

# Constants for `Wake Up` game.
ZIP = "219"
ZAP = "249"
ZOP = "209"

class D15C0RD(commands.Bot):
    def __init__(self, bot, Message):
        self.bot = bot
        self.message_queue = bot.message_queue
        self.Message = Message
        self.flash_data = bot.flash_data
        self.discord_token = bot.discord_token

        intents = discord.Intents(**bot.bot_init_data["intents"])
        command_prefix = bot.bot_init_data["command_prefix"]

        super().__init__(command_prefix=command_prefix, intents=intents)

    async def start(self):
        await super().start(self.discord_token)
        await self.message_queue.put(self.Message(ZIP, "game"))
        self.flash_data.set(ZIP)  # Use the set method

    async def close(self):
        await super().close()

    async def on_ready(self):
        home_channel = self.get_channel(self.bot.home_channel_id)
        if home_channel is not None:
            await home_channel.send("Honey! I'm home!")
        else:
            self.flash_data.set(f"Error: Could not find a channel with ID {self.bot.home_channel_id}")  # Use the set method
            print(f"Error: Could not find a channel with ID {self.bot.home_channel_id}")
            quit()

    async def process_message_queue(self):
        while True:
            message = await self.message_queue.get()
            if message.type == "game":
                print(f"Processing game message: {message.content}")
                if message.content == ZIP:
                    await self.message_queue.put(self.Message(ZAP, "game"))
                    self.flash_data.set(ZAP)  # Use the set method
                elif message.content == ZAP:
                    await self.message_queue.put(self.Message(ZOP, "game"))
                    self.flash_data.set(ZOP)  # Use the set method
                elif message.content == ZOP:
                    print("Game sequence successful")
            else:
                print(f"Processing message: {message.content}")
            self.message_queue.task_done()

    async def on_message(self, message):
        if message.content == self.flash_data.get_flash_and_reset():  # Use the get_flash_and_reset method
            if message.content == ZIP:
                await self.message_queue.put(self.Message(ZAP, "game"))
                self.flash_data.set(ZAP)  # Use the set method
            elif message.content == ZAP:
                await self.message_queue.put(self.Message(ZOP, "game"))
                self.flash_data.set(ZOP)  # Use the set method
            else:
                self.flash_data.set("You Lost")  # Use the set method
        else:
            print(f"Received message: {message}")
            await self.message_queue.put(self.Message(message, "message"))

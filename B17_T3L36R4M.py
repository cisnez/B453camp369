#B17_73L36R4M.py
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# Constants for `Wake Up` game.
ZIP = "219"
ZAP = "249"
ZOP = "209"

class T3L36R4M:
    def __init__(self, api_id, api_hash, message_queue, Message, flash_data):
        self.message_queue = message_queue
        self.Message = Message
        self.flash_data = flash_data

        self.api_id = api_id
        self.api_hash = api_hash

        self.client = Client("bot", api_id=self.api_id, api_hash=self.api_hash)

        self.register_handlers()

    def register_handlers(self):
        @self.client.on_message(filters.text)
        async def handle_message(client: Client, message: Message):
            print(f"Received message: {message.text}")
            await self.message_queue.put(self.Message(message.text, "message"))

        asyncio.create_task(self.process_message_queue())

    async def process_message_queue(self):
        while True:
            message = await self.message_queue.get()
            text = message.content.lower()

            # Check if the message starts with a command to generate an image
            if text.startswith(".art "):
                prompt = text[9:]  # Extract the prompt text
                image_path = await text_to_image_sd(self, prompt)
                if image_path:
                    await message.reply_photo(photo=open(image_path, "rb"))
                else:
                    await message.reply("Failed to generate the image.")
            elif text == "hi":
                await message.reply("Hello!\n")
            elif text == self.flash_data.get_and_reset():
                if text == ZIP:
                    await message.reply(ZAP)  # Respond ZAP to received ZIP
                    self.flash_data.set(ZAP)
                    await self.message_queue.put(self.Message(ZAP, "game"))
                elif text == ZAP:
                    await message.reply(ZOP)  # Respond ZOP to received ZAP
                    self.flash_data.set(ZOP)
                    await self.message_queue.put(self.Message(ZOP, "game"))
            else:
                self.flash_data.set("You Lost")

            self.message_queue.task_done()

    def run(self):
        self.client.run()

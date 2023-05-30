#B17_73L36R4M.py
from pyrogram import Client

# Constants for `Wake Up` game.
ZIP = "219"
ZAP = "249"
ZOP = "209"

class T3L36R4M:
    def __init__(self, data, api_id, api_hash):
        self.data = data
        self.api_id = api_id
        self.api_hash = api_hash

        self.client = Client("bot", api_id=self.api_id, api_hash=self.api_hash)

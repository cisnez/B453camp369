#B17_M3554635.py
import asyncio

class M3554635:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def put(self, message):
        await self.queue.put(message)

    async def get(self):
        return await self.queue.get()

    def task_done(self):
        self.queue.task_done()

    class Message:
        def __init__(self, content, type):
            self.content = content
            self.type = type

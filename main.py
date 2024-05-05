from telegram import Bot
import asyncio

group_id = "-4127805355"

bot_token = "7179515450:AAF5dJ4xqcyHxwICuBp3DlDwRCI5ydiTYWQ"

message = "Hi, I am from Python"

bot = Bot(token=bot_token)

async def send_message(text, group_id):
    async with bot:
        await bot.send_message(text=text, chat_id=group_id)

async def main():
    await send_message(text=message, group_id=group_id)

asyncio.run(main())

from pyrogram import Client

app = Client("my_userbot", api_id="YOUR_API_ID", api_hash="YOUR_API_HASH")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello, I'm a userbot!")

app.run()

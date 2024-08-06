from pyrogram import Client

app = Client(
    "my_userbot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("SESSION_STRING")
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello, I'm a userbot!")

app.run()

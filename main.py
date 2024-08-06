from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message
import os
from config import *
app = Client(
    "my_userbot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("SESSION_STRING")
)

message_counts = {}

# Helper function to send a default warning message
async def send_warning(client, chat_id, user_name, warns):
    default_text = f"""
<b>Hello, {user_name}!</b>
<i>This is an automated message. Please do not spam. You have {warns} warnings.</i>
"""
    await client.send_message(chat_id, default_text, parse_mode="html")

# PM Protection handler
@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def anti_pm_handler(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    # Initialize message counts for the user if not already done
    if user_id not in message_counts:
        message_counts[user_id] = 0

    message_counts[user_id] += 1
    warns = message_counts[user_id]

    # Send a warning message
    await send_warning(client, chat_id, user_name, warns)

    # Check if the user needs to be blocked
    if warns > PM_LIMIT:
        await client.send_message(
            chat_id,
            "<b>This is your last warning. You will be blocked now.</b>",
            parse_mode="html"
        )
        await client.block_user(user_id)
        del message_counts[user_id]

# Command to enable/disable PM protection
@app.on_message(filters.command(["antipm", "anti_pm"], prefixes="!") & filters.me)
async def toggle_pm_protection(client, message: Message):
    if len(message.command) == 1:
        status = "enabled" if os.getenv("PM_PROTECTION_ENABLED", "true") == "true" else "disabled"
        await message.reply(f"PM protection is currently {status}.")
    elif message.command[1] in ["enable", "on", "true"]:
        os.environ["PM_PROTECTION_ENABLED"] = "true"
        await message.reply("PM protection enabled.")
    elif message.command[1] in ["disable", "off", "false"]:
        os.environ["PM_PROTECTION_ENABLED"] = "false"
        await message.reply("PM protection disabled.")
    else:
        await message.reply("Usage: !antipm [enable|disable]")

# Command to enable/disable spam reporting
@app.on_message(filters.command(["antipm_report"], prefixes="!") & filters.me)
async def toggle_spam_reporting(client, message: Message):
    if len(message.command) == 1:
        status = "enabled" if os.getenv("SPAM_REPORTING_ENABLED", "false") == "true" else "disabled"
        await message.reply(f"Spam reporting is currently {status}.")
    elif message.command[1] in ["enable", "on", "true"]:
        os.environ["SPAM_REPORTING_ENABLED"] = "true"
        await message.reply("Spam reporting enabled.")
    elif message.command[1] in ["disable", "off", "false"]:
        os.environ["SPAM_REPORTING_ENABLED"] = "false"
        await message.reply("Spam reporting disabled.")
    else:
        await message.reply("Usage: !antipm_report [enable|disable]")

# Command to enable/disable user blocking
@app.on_message(filters.command(["antipm_block"], prefixes="!") & filters.me)
async def toggle_user_blocking(client, message: Message):
    if len(message.command) == 1:
        status = "enabled" if os.getenv("USER_BLOCKING_ENABLED", "false") == "true" else "disabled"
        await message.reply(f"User blocking is currently {status}.")
    elif message.command[1] in ["enable", "on", "true"]:
        os.environ["USER_BLOCKING_ENABLED"] = "true"
        await message.reply("User blocking enabled.")
    elif message.command[1] in ["disable", "off", "false"]:
        os.environ["USER_BLOCKING_ENABLED"] = "false"
        await message.reply("User blocking disabled.")
    else:
        await message.reply("Usage: !antipm_block [enable|disable]")

# Commands to approve or disapprove users
@app.on_message(filters.command(["a"], prefixes="!") & filters.me)
async def add_contact(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    os.environ[f"ALLOW_USERS_{chat_id}"] = str(user_id)
    await message.reply("User approved!")

@app.on_message(filters.command(["d"], prefixes="!") & filters.me)
async def del_contact(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    os.environ[f"DISALLOW_USERS_{chat_id}"] = str(user_id)
    os.environ.pop(f"ALLOW_USERS_{chat_id}", None)
    await message.reply("User disapproved!")

app.run()

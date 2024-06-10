import logging
import os
import importlib
from logging.handlers import RotatingFileHandler
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsSearch
from dotenv import load_dotenv
from telethon import Button, TelegramClient, events

# load the .env file
load_dotenv()

# Create the client and connect
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
bot = TelegramClient('bot', int(api_id), api_hash).start(bot_token=bot_token)


try:
    # Logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # RotatingFileHandler
    max_log_size_mb = 5  # Set your desired maximum log size in megabytes
    file_handler = RotatingFileHandler('./bot.log', maxBytes=max_log_size_mb * 1024 * 1024, backupCount=1)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

    # commands_dir = os.path.join(os.path.dirname(__file__), 'Commands')
    # commands = {}
    #
    # for folderName in os.listdir(commands_dir):
    #     if folderName.endswith('.py') and folderName != '__init__.py':
    #         command_name = os.path.splitext(folderName)[0]
    #         command = importlib.import_module(f'Commands.{command_name}')
    #         commands[command_name] = command
    #
    # logging.info("Main script runs successfully, Bot is working")

    # Start command



    group_id = 'https://t.me/LLLLLLLLLPotcghv'  # Use the group ID or username

    async def get_full_channel(group_id):

        # Get full channel info
        full_channel = await bot(GetFullChannelRequest(group_id))

        print(full_channel)

    async def get_admins(group_id):
        # Get all participants who are admins
        admins = await bot.get_participants(group_id, filter=ChannelParticipantsAdmins)

        # Print admin details
        for admin in admins:
            print(f"Admin: {admin.first_name} {admin.last_name} ({admin.id})")


    @bot.on(events.NewMessage(pattern='/start'))
    async def start(event):
        sender = await event.get_sender()
        await get_admins(group_id)
        await get_full_channel(group_id)
        limit = 100
        offset = 0
        all_participants = []

        while True:
            participants = await bot(GetParticipantsRequest(
                channel=group_id,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not participants.users:
                break
            all_participants.extend(participants.users)
            offset += len(participants.users)

        if sender in all_participants:
            await event.respond("Welcome!")
        else:
            await event.respond(
                "Join the group",
                buttons=[
                    [Button.url("Join Group", "https://t.me/LLLLLLLLLPotcghv")]
                ])




    bot.run_until_disconnected()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")

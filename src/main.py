import logging
import os
import importlib
from logging.handlers import RotatingFileHandler
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsSearch, PeerChannel
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

    group_id = 'https://t.me/LLLLLLLLLPotcghv'  # Use the group ID or username


    @bot.on(events.NewMessage(pattern='/start'))
    async def start(event):
        sender = await event.get_sender()
        user_id = sender.id

        limit = 100
        offset = 0
        all_participants = []

        # Get all participants who are admins
        admins = await bot.get_participants(group_id, filter=ChannelParticipantsAdmins)


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

        buttons = [
                        [Button.inline("السنة الأولى", data="first_class")],
                        [Button.inline("السنة الثانية", data="second_class")],
                        [Button.inline("السنة الثالثة", data="third_class")],
                        [Button.inline("السنة الرابعة", data="forth_class")]
                    ]

        # بعرف فينا نختصر هدول الحلقات بس عفتها مشان عدلها بعدين
        if sender in all_participants and sender in admins and user_id == 1257415932:
            await event.respond("أهلا وسهلا بك في البوت الخاص بجميع مقررات كلية الحقوق في جامعة حلب")
            await event.respond("اختر السنة:", buttons = buttons)

        elif sender in all_participants:
            await event.respond("أهلا وسهلا بك في البوت الخاص بجميع مقررات كلية الحقوق في جامعة حلب")
            await event.respond("اختر السنة:", buttons = buttons)

        else:
            await event.respond("عذرا, يبدو أنك لست منضماً إلى المجموعة الخاصة بنا\n\nأرجو منك الانضمام بواسطة الزر الموجود أسفل هذه الرسالة", buttons=[[Button.url("الانضمام", "https://t.me/LLLLLLLLLPotcghv")]])

    # Make callback query handlers for the buttons
    @bot.on(events.CallbackQuery())
    async def callback_query_handler(event):
        data = event.data
        if data == b'first_class':
            await bot.edit_message(event.sender_id, event.message_id, "اختر الفصل", buttons=[
                [Button.inline("الفصل الأول", data="first_semester_st")],
                [Button.inline("الفصل الثاني", data="second_semester_st")],
                [Button.inline("• الرجوع •", data="backMain")]
            ])
        elif data == b'second_class':
            await bot.edit_message(event.sender_id, event.message_id, "اختر الفصل", buttons=[
                [Button.inline("الفصل الأول", data="first_semester_nd")],
                [Button.inline("الفصل الثاني", data="second_semester_nd")],
                [Button.inline("• الرجوع •", data="backMain")]
            ])
        elif data == b'third_class':
            await bot.edit_message(event.sender_id, event.message_id, "اختر الفصل", buttons=[
                [Button.inline("الفصل الأول", data="first_semester_rd")],
                [Button.inline("الفصل الثاني", data="second_semester_rd")],
                [Button.inline("• الرجوع •", data="backMain")]
            ])
        elif data == b'forth_class':
            await bot.edit_message(event.sender_id, event.message_id, "اختر الفصل", buttons=[
                [Button.inline("الفصل الأول", data="first_semester_th")],
                [Button.inline("الفصل الثاني", data="second_semester_th")],
                [Button.inline("• الرجوع •", data="backMain")]
            ])
        elif data == b'backMain':
            await bot.edit_message(event.sender_id, event.message_id, "اختر السنة", buttons=[
                [Button.inline("السنة الأولى", data="first_class")],
                [Button.inline("السنة الثانية", data="second_class")],
                [Button.inline("السنة الثالثة", data="third_class")],
                [Button.inline("السنة الرابعة", data="forth_class")]
            ])


    bot.run_until_disconnected()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")


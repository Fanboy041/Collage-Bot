import logging
import os
import json
import base64
# import importlib
from logging.handlers import RotatingFileHandler
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsSearch, InputDocument
from dotenv import load_dotenv
from telethon import Button, TelegramClient, events, types
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

    # Load uploaded files from JSON, or create an empty list if none exist
    try:
        with open('uploaded_files.json', 'r') as file:
            uploaded_files = json.load(file)
    except FileNotFoundError:
        uploaded_files = []

    upload_status = {}

    @bot.on(events.NewMessage(pattern='/upload'))
    async def start_upload_process(event):
        await event.respond("Please upload one or more files. Press 'Done' when finished.")
        upload_status[event.chat_id] = {'files': [], 'done': False}
        await show_done_button(event.chat_id)

    # Maek "Done" button.text in a custom keyboard
    async def show_done_button(chat_id):
        keyboard = [
            [
                Button.text('Done', resize=True, single_use=True),
            ]
        ]
        await bot.send_message(chat_id, 'Press "Done" when finished uploading files.', buttons=keyboard)


    @bot.on(events.NewMessage(func=lambda e: e.text and e.text.lower() == 'done'))
    async def process_upload(event):
        try:
            chat_id = event.chat_id
            user_upload_status = upload_status.get(chat_id, {})
            files = user_upload_status.get('files', [])

            if files:
                uploaded_files.extend(files)
                await event.respond("Files uploaded successfully. Use /download to get the files.", buttons=Button.clear())

                with open('uploaded_files.json', 'w') as file:
                    json.dump(uploaded_files, file)

                upload_status.pop(chat_id, None)
            else:
                await event.respond("No files uploaded. Use /upload to upload files.", buttons=Button.clear())

        except Exception as e:
            print(f"Error in process_upload: {e}")
            await event.respond("An error occurred. Please try again.")


    @bot.on(events.NewMessage(func=lambda e: e.message.document))
    async def handle_document(event):
        chat_id = event.chat_id
        user_upload_status = upload_status.get(chat_id, {})

        if not user_upload_status.get('done', False):
            file_id = event.message.document.id
            access_hash = event.message.document.access_hash
            file_reference = base64.b64encode(event.message.document.file_reference).decode('utf-8')

            file_data = (file_id, access_hash, file_reference)
            user_upload_status['files'].append(file_data)
        else:
            await event.respond("You have already pressed 'Done'. Use /upload to start a new upload session.")


    @bot.on(events.NewMessage(pattern='/download'))
    async def download_handler(event):
        try:
            if uploaded_files:
                for file_data in uploaded_files:
                    file_id, access_hash, file_reference = file_data
                    file_reference = base64.b64decode(file_reference.encode('utf-8'))
                    file = InputDocument(id=file_id, access_hash=access_hash, file_reference=file_reference)
                    await bot.send_file(event.chat_id, file)
            else:
                await event.respond("No files have been uploaded yet.")
        except Exception as e:
            print(f"Error in download_handler: {e}")
            await event.respond("An error occurred while downloading the files.")


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
[Button.inline("السنة الأولى", data="first_class"),
Button.inline("السنة الثانية", data="second_class")],
[Button.inline("السنة الثالثة", data="third_class"),
Button.inline("السنة الرابعة", data="forth_class")],
[Button.inline("اختياري", data="optional")]
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
[Button.inline("السنة الأولى", data="first_class"),
Button.inline("السنة الثانية", data="second_class")],
[Button.inline("السنة الثالثة", data="third_class"),
Button.inline("السنة الرابعة", data="forth_class")],
[Button.inline("اختياري", data="optional")]
])
        elif data == b'backsemester':
            await bot.edit_message(event.sender_id, event.message_id, "اختر الفصل", buttons=[
[Button.inline("الفصل الأول", data="first_semester_st")],
[Button.inline("الفصل الثاني", data="second_semester_st")],
[Button.inline("• الرجوع •", data="backMain")]
])


        elif data == b'first_semester_st':
            await bot.edit_message(event.sender_id, event.message_id, "اختر المادة", buttons=[
[Button.inline("تاريخ القانون", b"History of law"),
Button.inline("قانون دستوري", b"Constitutional law")],
[Button.inline("نظم سياسية", b"Political systems"),
Button.inline("مدخل إلى علم القانون", b"Introduction to the science of law")],
[Button.inline("علم الإجرام والعقاب", b"Criminology and punishment"),
Button.inline("علاقات دولية ودبلوماسية", b"International relations and diplomacy")],
[Button.inline("لغة إنكليزية 1 / فرنسية 1", b"English language 1 / French 1"),
Button.inline("لغة إنكليزية 2 / فرنسية 2", b"English language 2 / French 2")],
[Button.inline("لغة عريبة", b"Arabic language"),
Button.inline("ثقافة قومية", b"National culture")],
[Button.inline("شريعة إسلامية", b"Islamic law"),
Button.inline("منظمات دولية", b"International organizations")],
[Button.inline("اقتصاد سياسي", b"Political economy"),
Button.inline("تشريعات اجتماعية تعاون", b"Social cooperation legislation")],
[Button.inline("• الرجوع •", data="backsemester")]
])
        elif data == b'first_semester_nd':
            await bot.edit_message(event.sender_id, event.message_id, "اختر المادة", buttons=[
[Button.inline("مصادر التزام", b"Sources of commitment"),
Button.inline("أحكام التزام", b"Commitment provisions")],
[Button.inline("شركات تجارية", b"Commercial companies"),
Button.inline("أحوال شخصية مواريث", b"Personal status Inheritance")],
[Button.inline("مالية عامة", b"Public finances"),
Button.inline("قانون دولي عام", b"Public international law")],
[Button.inline("تشريعات اجتماعية قانون العمل", b"Social legislation Labor law"),
Button.inline("لغة إنكليزية / لغة فرنسية 3", b"English / French language 3")],
[Button.inline("لغة إنكليزية /لغة فرنسية 4", b"English / French language 4"),
Button.inline("قانون إداري 1", b"Administrative law 1")],
[Button.inline("قانون إداري 2", b"Administrative law 2"),
Button.inline("قانون العقوبات العام", b"General penal code")],
[Button.inline("مدخل قانون تجاري ( تاجر ومتجر )", b"Introduction to commercial law (merchant and store)")],
[Button.inline("• الرجوع •", data="backsemester")]
])
        elif data == b'first_semester_rd':
            await bot.edit_message(event.sender_id, event.message_id, "اختر المادة", buttons = [
[Button.inline("عقود مسماة", b"Named Contracts"), Button.inline("إدارة عامة", b"Public Administration")],
[Button.inline("أصول محاكمات مدنية 1", b"Civil Procedure Procedures 1"), Button.inline("أصول محاكمات مدنية 2", b"Civil Procedure Procedures 2")],
[Button.inline("أوراق تجارية وعمليات مصرفية", b"Commercial Papers and Banking Operations"), Button.inline("أحوال شخصية زواج طلاق", b"Personal Status Marriage Divorce")],
[Button.inline("قانون دولي خاص 1 جنسية", b"Private International Law 1 Nationality"), Button.inline("القضاء الإداري", b"Administrative Judiciary")],
[Button.inline("قانون تجاري ( بحري جوي )", b"Commercial Law (Naval Air)"), Button.inline("قانون عقوبات خاص 1", b"Special Penal Code 1")],
[Button.inline("قانون عقوبات خاص 2", b"Special Penal Code 2"), Button.inline("التحكيم في العلاقات الخاصة", b"arbitration in private relations")],
[Button.inline("الأدلة القضائية والطب الشرعي", b"judicial evidence and forensic medicine"), Button.inline("القانون الدولي البيئي", b"international environmental law")],
[Button.inline("المرافق العامة", b"public utilities"), Button.inline("قانون الأسواق والأوراق المالية", b"markets and securities law")],
[Button.inline("تأمينات اجتماعية", b"social insurance"), Button.inline("قانون جزائي دولي ( تسليم مجرمين )", b"international criminal law (extradition of criminals)")],
[Button.inline("قانون دولي إنساني", b"international humanitarian law"), Button.inline("إدارة محلية", b"local administration")],
[Button.inline("تشريعات مصرفية", b"banking legislation"), Button.inline("حقوق الإنسان والحريات العامة", b"human rights and public freedoms")],
[Button.inline("• الرجوع •", data="backsemester")]
])
        elif data == b'first_semester_th':
            await bot.edit_message(event.sender_id, event.message_id, "اختر المادة", buttons = [
[Button.inline("تشريع ضريبي", b"Tax legislation"), Button.inline("أصول محاكمات جزائية 1", b"Principles of criminal trials 1")],
[Button.inline("أصول محاكمات جزائية 2", b"Principles of criminal trials 2"), Button.inline("أصول الفقه الإسلامي", b"Principles of Islamic jurisprudence")],
[Button.inline("مدني 1 حقوق عينية أصلية", b"Civil 1 Original real rights"), Button.inline("مدني 2 حقوق عينية تبعية", b"Civil 2 Accessory real rights")],
[Button.inline("أصول التنفيذ", b"Principles of implementation"), Button.inline("قانون دولي خاص 2 تنازع قوانين", b"Private international law 2 Conflict of laws")],
[Button.inline("عقود تجارية", b"Commercial contracts")],
[Button.inline("• الرجوع •", data="backsemester")]
])
        elif data == b'optional':
            await bot.edit_message(event.sender_id, event.message_id, "اختر المادة", buttons = [
[Button.inline("قانون مدني مقارن", b"Comparative civil law"), Button.inline("قانون أحداث جانحين", b"Juvenile delinquent law")],
[Button.inline("القانون الدولي لحقوق الإنسان", b"International human rights law"), Button.inline("نزع الملكية للمنفعة العامة", b"Expropriation for public benefit")],
[Button.inline("قانون التجارية الدولية", b"International commercial law"), Button.inline("النظام القضائي في الإسلام", b"Judicial system in Islam")],
[Button.inline("قانون العقوبات الاقتصادية", b"Economic penal law"), Button.inline("القانون الدولي الاقتصادي", b"International economic law")],
[Button.inline("رقابة مالية وإدارية", b"Financial and administrative control"), Button.inline("الملكية التجارية والصناعية", b"Commercial and industrial property")],
[Button.inline("قانون حماية المستهلك", b"Consumer protection law"), Button.inline("القانون الجزائي للأعمال", b"Business criminal law")],
[Button.inline("القانون الدبلوماسي", b"Diplomatic law"), Button.inline("القضاء الدستوري", b"Constitutional judiciary")],
[Button.inline("نقود ومصارف وتشريعات مصرفية", b"Money, banking and banking legislation"), Button.inline("حماية حقوق المكلية الفكرية", b"Protection of intellectual property rights")],
[Button.inline("تشريعات جزائية خاصة", b"Special penal legislation"), Button.inline("قانو النطاق الدولي", b"International law")],
[Button.inline("التشريع البيئي", b"Environmental legislation"), Button.inline("التحكيم التجاري", b"Commercial arbitration")],
[Button.inline("• الرجوع •", data="backMain")]
])
    bot.run_until_disconnected()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")


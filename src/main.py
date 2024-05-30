import telebot, logging
import os
import importlib
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

try:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    max_log_size_mb = 5
    file_handler = RotatingFileHandler('./bot.log', maxBytes=max_log_size_mb * 1024 * 1024, backupCount=1)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

    commands_dir = os.path.join(os.path.dirname(__file__), 'Commands')
    commands = {}

    for foldername in os.listdir(commands_dir):
        if foldername.endswith('.py') and foldername != '__init__.py':

            command_name = os.path.splitext(foldername)[0]
            command = importlib.import_module(f'Commands.{command_name}')
            commands[command_name] = command

    logging.info("Main script runs successfully, Bot is working")

    # Start command
    @bot.message_handler(commands=['start'])
    def handle_start_command(message):
        if 'startCommand' in commands:
            commands['startCommand'].start_command(message, bot)




    bot.infinity_polling()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")

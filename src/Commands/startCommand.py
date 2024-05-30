from Database.MongoDB import owner_collection, save_owner, user_collection, save_user, get_owner

def start_command(message, bot):
    if message.chat.type == "private":

        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if last_name:
            full_name = first_name + " " + last_name
        else:
            full_name = first_name

        username = message.from_user.username
        chat_id = message.chat.id

        if owner_collection.count_documents({}) == 0:
            save_owner(full_name, username, chat_id)
            bot.send_message(message.chat.id, f"أهلا <b>{full_name}</b>\nلقد أصبحت مالك البوت من الآن فصاعدا", parse_mode='HTML')

        else:
            total_users = user_collection.count_documents({}) + 1
            save_user(full_name, username, chat_id, total_users)

            if message.chat.id == get_owner()['chat_id']:
                bot.send_message(message.chat.id, f"مرحبا أيها المالك, <b>{full_name}</b>. 🌹", parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, f"مرحبًا، <b>{full_name}</b>!\n\nشكرًا لك على التفاعل مع الروبوت الخاص بنا. نحن متحمسون لوجودك معنا. 🌹", parse_mode='HTML')
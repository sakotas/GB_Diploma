import telebot
from telebot import types
from dictionary import MESSAGES  # Импортируем словарь сообщений

# Токен бота
bot = telebot.TeleBot('6702120335:AAFpic7QYsukggZ--9xp6s8F-PERJCl7c5Q')

# Текущий язык пользователя
user_language = {}

def send_start_message(user_id):
    """Отправляет стартовое сообщение с учетом языка пользователя."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    greet_btn = types.InlineKeyboardButton(MESSAGES['buttons']['greet'][user_language[user_id]])
    change_lang_btn = types.InlineKeyboardButton(MESSAGES['buttons']['change_lang'][user_language[user_id]])
    markup.add(greet_btn, change_lang_btn)
    bot.send_message(user_id, MESSAGES['start'][user_language[user_id]], reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    # Предполагаем, что пользователь говорит по-русски по умолчанию
    user_language[message.from_user.id] = 'ru'
    send_start_message(message.from_user.id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, 'ru')  # Получаем язык пользователя, по умолчанию 'ru'

    if message.text == MESSAGES['buttons']['change_lang']['ru']:
        user_language[user_id] = 'en'  # Переключаем язык на английский
        send_start_message(user_id)  # Перезапускаем стартовое сообщение
        return
    elif message.text == MESSAGES['buttons']['change_lang']['en']:
        user_language[user_id] = 'ru'  # Переключаем язык на русский
        send_start_message(user_id)
        return

    if message.text == MESSAGES['buttons']['greet'][lang]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        register_btn = types.InlineKeyboardButton(MESSAGES['buttons']['register'][lang])
        send_photo_btn = types.InlineKeyboardButton(MESSAGES['buttons']['send_photo'][lang])
        back_btn = types.InlineKeyboardButton(MESSAGES['buttons']['back'][lang])
        markup.add(register_btn, send_photo_btn, back_btn)
        bot.send_message(user_id, MESSAGES['greet'][lang], reply_markup=markup)

    elif message.text in [MESSAGES['buttons']['register'][lang], MESSAGES['buttons']['send_photo'][lang]]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_btn = types.InlineKeyboardButton(MESSAGES['buttons']['back'][lang])
        markup.add(back_btn)
        if message.text == MESSAGES['buttons']['register'][lang]:
            bot.send_message(user_id, MESSAGES['register'][lang], reply_markup=markup)
        else:
            bot.send_message(user_id, MESSAGES['send_photo'][lang], reply_markup=markup)

    elif message.text == MESSAGES['buttons']['back'][lang]:
        send_start_message(user_id)  # Возвращаем пользователя к началу диалога

bot.polling(none_stop=True, interval=0)
import telebot
from decouple import config


BOT_TOKEN = config('TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'как дела?':
        bot.reply_to(message, 'Нормально, ты как?')
    elif message.text == 'привет':
        bot.reply_to(message, "Привет, Привет, Привет!")
    elif message.text == 'норм':
        bot.reply_to(message, 'Ну и отлично')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю!')


bot.infinity_polling()

import telebot
import buttons
import database
import translator


bot = telebot.TeleBot('2047910242:AAFYo7NrHUcpWY2Wl1IeJiu-Dr7dzvFG2R0')

@bot.message_handler(commands=['start'])
def start_command(message):
  database.createDatabase();
  bot.send_message(message.chat.id, "Hello this is a tranlator bot! \n /set for setting languages")


@bot.message_handler(commands=['set'])
def choose_command(message):
  bot.send_message(message.chat.id, "Choose the language of your text:", reply_markup = buttons.getFromLangs());

@bot.message_handler(content_types=['text'])
def text_handler(message):
  if(message.text in database.fromLangs.values()):
    database.fromLang = message.text;
    bot.send_message(message.chat.id, "Choose the language of translation:", reply_markup = buttons.getToLangs());
  elif(message.text in database.toLangs.values()):
    database.toLang = message.text;
    bot.send_message(message.chat.id, "Print several text!", reply_markup = telebot.types.ReplyKeyboardRemove());
  else:
    if(database.fromLang == None or database.toLang == None):
      return bot.send_message(message.chat.id, "Firstly choose the languages by /set command")
    bot.send_message(message.chat.id, translator.get(message.text))


bot.polling()

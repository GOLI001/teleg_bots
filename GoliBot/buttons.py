from telebot import types
import database

def getFromLangs():
  fromLangList = types.ReplyKeyboardMarkup(resize_keyboard = True)
  for i in database.fromLangs:
    # print(i);
    fromLangList.add(types.KeyboardButton(text = database.fromLangs[i]))
  return fromLangList;


def getToLangs():
  toLangList = types.ReplyKeyboardMarkup(resize_keyboard = True)
  for i in database.toLangs:
    toLangList.add(types.KeyboardButton(text = database.toLangs[i]))
  return toLangList;
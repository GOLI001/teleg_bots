from googletrans import Translator
import database

translator = Translator()

fr = '' 
to = ''

def encode():
  global fr, to
  frsize = len(database.fromLang)
  tosize = len(database.toLang)
  fr = database.fromLang[5:frsize].lower()
  to = database.toLang[3:tosize].lower()

def get(message):
	encode()
	value = translator.translate(message, src=fr, dest=to);
	# print(value);
	return value.text;
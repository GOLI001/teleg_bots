from telebot import types

fromLang = None
toLang = None

fromLangs = {}
toLangs = {}

def createDatabase():
	fromLangs[0] = 'from Russian'
	fromLangs[1] = 'from English'
	fromLangs[2] = 'from Kazakh'
	fromLangs[3] = 'from French'
	fromLangs[4] = 'from Spanish'
	fromLangs[5] = 'from Turkish'

	toLangs[0] = 'to Russian'
	toLangs[1] = 'to English'
	toLangs[2] = 'to Kazakh'
	toLangs[3] = 'to French'
	toLangs[4] = 'to Spanish'
	toLangs[5] = 'to Turkish'
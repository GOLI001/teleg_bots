from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#START BUTTON
random = KeyboardButton('💎 Случайное произведение')
all_p = KeyboardButton('📃 Все произведение')
referal = KeyboardButton('🔗 Реферал')
authors = KeyboardButton('👤 Авторы')
stats = KeyboardButton('-📊-')
mail = KeyboardButton('Тарату')
# add = KeyboardButton('📄 Өлең ұсыну')
subscribe = KeyboardButton('✅ Подписаться')

start = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5).add(random, all_p).add( authors, subscribe)
start_a = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5).add(random, all_p, mail).add( authors, subscribe, stats)

# CONFIRM BUTTON
confirmButton = InlineKeyboardMarkup().add(InlineKeyboardButton('✅ Ұсыну', callback_data='confirm'), InlineKeyboardButton('❌ Өшіру', callback_data='cancel' ) )

#ADDPOEM BUTTON
addPoemButton = InlineKeyboardMarkup().add(InlineKeyboardButton('✅ Қосу', callback_data='add'), InlineKeyboardButton('❌ Өшіру', callback_data='delete' ) )

#ADDPOEM BUTTON
typeButton = InlineKeyboardMarkup().add(InlineKeyboardButton('Напишите /start для запуска бота 👤', callback_data='fromauthors'))

def getPdfButton(poem_id, random=False):
	pdfButton = InlineKeyboardMarkup()
	if random:
		pdfButton.add(InlineKeyboardButton('💎 Другая случайная произведение ', callback_data='random'))
	pdfButton.add(InlineKeyboardButton('⬇️ PDF', callback_data='pdf|'+str(poem_id)))
	return pdfButton
def pageination(identificator, page, maxpage, perpage, count, showAuthorInfo=False):
	pp = perpage+1; mp = perpage-1;
	authorsButton = InlineKeyboardMarkup(row_width=5)
	if page>2:
		authorsButton.insert(InlineKeyboardButton('1 ...', callback_data='{}|1'.format(identificator)) )
		authorsButton.insert(InlineKeyboardButton('<<', callback_data='{}|{}'.format(identificator, page-1)) )
	elif page>1: 
		authorsButton.insert(InlineKeyboardButton('<<', callback_data='{}|{}'.format(identificator, page-1)) )
	authorsButton.insert(InlineKeyboardButton('• {} •'.format(page), callback_data='_'))
	if count == pp: 
		authorsButton.insert(InlineKeyboardButton('>>', callback_data='{}|{}'.format(identificator, page+1)) )
	if page<(maxpage-1):
		authorsButton.insert(InlineKeyboardButton('... {}'.format(maxpage), callback_data='{}|{}'.format(identificator, maxpage)) )
	if showAuthorInfo:
		authorsButton.add(InlineKeyboardButton('🌐 Биография автора', url='https://www.google.kz/search?q='+showAuthorInfo))
	return authorsButton


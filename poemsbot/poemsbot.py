import libs , math
import keyboards as kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

bot_token = 
bot_username = "zolotoivek_bot"

bot = Bot(token=bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage = MemoryStorage())

#States
class Form(StatesGroup):
    message_id = State()
    confirm = State()
class newPoem(StatesGroup):
    name = State()
    author = State()
    content = State()
    confirm = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    try:
        ref=message.text.split()[1]
        await bot.send_message(ref, "💰 Құттықтаймыз, сіздің рефералка-мен бір адам кірді!")
    except IndexError:
        ref = '0' 
    libs.newUser(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, ref)
    keyboard = kb.start_a if libs.isAdmin(message.chat.id) == 1 else kb.start
    await message.answer("📎 Напишите имя автора или имя произведения\n\n<b>👋🏻 Добро пожаловать в наш бот!\n\n</b>""<b>Тут вы можете найти своих любимых русских писателей Золотого века🤗</b>" , reply_markup=keyboard)

# @dp.message_handler(lambda message: message.text == '📄 Өлең ұсыну')
# async def process_name(message: types.Message, state: FSMContext):
#     await newPoem.name.set()
#     await message.answer('<b>Өлең атын жазыңыз:</b>')
@dp.message_handler(state=newPoem.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as npoem:
        npoem['name'] = message.text
    await newPoem.next()
    await message.answer('<b>Напишите имя автора:</b>')
@dp.message_handler(state=newPoem.author)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as npoem:
        npoem['author'] = message.text
    await newPoem.next()
    await message.answer('<b>Өлеңді жіберіңіз:</b>')
@dp.message_handler(state=newPoem.content)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as npoem:
        npoem['content'] = message.text
    await newPoem.next()
    await message.answer('<b>{}</b>\n<i>{}</i>\n\n{}'.format(npoem['name'], npoem['author'], npoem['content']), reply_markup=kb.confirmButton)
@dp.callback_query_handler(text_contains='confirm', state=newPoem.confirm)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as npoem:
        await bot.edit_message_text('<b>✅ Ұсынылды</b>', callback_query.from_user.id, callback_query.message.message_id)
        admins = libs.getAdmins()
        for admin in admins:
            try:
                await bot.send_message(admin[0], 'id:{}\n{}\n{}\n{}'.format(callback_query.from_user.id, npoem['name'], npoem['author'], npoem['content']), reply_markup=kb.addPoemButton)
            except:
                pass
            await asyncio.sleep(0.1)
    await state.finish()
@dp.callback_query_handler(lambda c: c.data and c.data == 'cancel', state='*')
async def process_callback_kb1btn1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text('<b>❌ Өшірілді</b>', callback_query.from_user.id, callback_query.message.message_id)
    await state.finish()
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    text = callback_query.message.text.split('\n', 3)
    id = text[0].split(':')[1].strip()
    name = text[1]
    author = text[2]
    content = text[3]
    libs.addPoem(name, author, content)
    await bot.send_message(id, '✅ <b>Сіз ұсынған өлең ботқа қосылды!</b>')
    await bot.edit_message_text('<b>✅ Қосылды</b>', callback_query.from_user.id, callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('delete'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.message.text.split('\n', 3)[0].split(':')[1].strip(), '<b>❌Сіз ұсынған өлең қосылмады!</b>\n\nМүмкін болған жайттар:\n• Өлең атында, немесе автордың аты-жөнінде қателік бар\n• Танымал өлең ботта бар\n• Ақын емес, әншілердің өлеңін ұсындыңыз\n\n<b>Кері байланыс: @maksutovnurda</b>')
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)







@dp.message_handler(lambda message: message.text == 'Тарату')
async def process_name(message: types.Message, state: FSMContext):
    if libs.isAdmin(message.chat.id):
        await Form.message_id.set()
        await message.answer('<b>Тарату хабарламасын жіберіңіз:</b>')
@dp.message_handler(content_types=['document', 'text', 'photo', 'audio', 'sticker', 'video'],state=Form.message_id)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = message.message_id
    await Form.next()
    await message.reply("Бастау үшін <b>'+++'</b> жіберіңіз, немесе <b>жаңа сообщение</b> жіберіңіз:\n\nТоқтату үшін <b>-</b> жіберіңіз.")
@dp.message_handler(content_types=['document', 'text', 'photo', 'audio', 'sticker', 'video'],state=Form.confirm)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == '+++':
        async with state.proxy() as data:
            users = libs.getUsers()
            count = 0
            await state.finish()
            await message.answer("Тарату басталды, <b>~{} минутта</b> толық аяқталады".format(round(len(users)/600), 1))
            for user in users:
                try:
                    await bot.copy_message(user[0], message.chat.id, data['message_id'], allow_sending_without_reply=True)
                    count += 1
                except BotBlocked as E:
                    libs.removeUser(user[0])
                except:
                    pass
                await asyncio.sleep(0.1)
            await message.answer("{} адамнан <b>{} адамға</b> жіберілді".format(len(users), count))
            libs.usersVacuum()
    elif message.text == '-':
        await message.answer("<b>Аяқталды</b>")
        await state.finish()
    else:
        async with state.proxy() as data:
            data['message_id'] = message.message_id
        await Form.confirm.set()
        await message.reply("Бастау үшін <b>'+++'</b> жіберіңіз, немесе <b>жаңа сообщение</b> жіберіңіз:\n\nТоқтату үшін <b>-</b> жіберіңіз.")


@dp.message_handler(commands=['unsubscribe'])
async def process_start_command(message: types.Message):        
    await message.answer('<b>✅ Вы отписались!</b>\n\n<i>Для повторной подписки:</i> /subscribe')
@dp.message_handler(commands=['subscribe'])
async def process_start_command(message: types.Message):        
    await message.answer('<b>Поздравляю </b> 🥳\nТеперь каждый день будете получать произведение\n\n<i>Для отписки:</fi> /unsubscribe')


@dp.message_handler()
async def echo_message(message: types.Message):
    if message.text.startswith('/o'): 
        answer = libs.getPoem(message.text[2:])
        if len(answer) > 4096:
            for i in range(0, len(answer), 4096):
                if i/4096+1 == math.ceil(len(answer)/4096): # IN LAST ITERATION
                    await message.answer(answer[i:i+4096], reply_markup=kb.getPdfButton(message.text[2:]))
                else:
                    await message.answer(answer[i:i+4096])
                await asyncio.sleep(0.1) # IF MESSAGE NOT LONG THAN 4096 chars
        else:
            await message.answer(answer, reply_markup=kb.getPdfButton(message.text[2:]))
    elif message.text.startswith('/a'):
        query = '-- {}'.format(libs.getAuthor(message.text[2:])[0])
        response = libs.searchPoem(1, query, True)
        await message.answer(response[0], reply_markup=response[1])
    elif message.text.startswith('/d'): 
        if libs.isAdmin(message.chat.id):
            libs.deletePoem(message.text[2:])
            await message.answer("✅ Өшірілді")
    elif message.text == '/contact':
        await message.answer('<i>• Боттан қателік тапсаңыз\n• Ұсынысыңыз болса\n• Өлең қосқыңыз келсе</i>\n\n<b>Telegram:</b> @maksutovnurda\n<b>Whatsapp:</b> wa.me/77025475495 (+77025475495)')
    elif message.text == '💎 Случайное произведение':
        poem = libs.getRandomPoem(); keyboard = kb.getPdfButton(poem[0], True)
        await message.answer("<b>{}</b>\n<i>{}</i>\n\n{}\n\nДругие произведение автора: /a{}".format(poem[1], poem[2], poem[3], poem[0]), reply_markup=keyboard)
    elif message.text == '📃 Все произведение':
        response = libs.searchPoem(1, "---")
        await message.answer(response[0], reply_markup=response[1])
    elif message.text == '🔗 Реферал':
        await message.answer("🔗 <b>Сіздің рефералкаңыз:</b> t.me/{}?start={}\n<i>Осыны басқаларға жіберіп бөлісіңіз. Осы сілтеме арқылы ботқа қанша адам қосқаныңызды көре аласыз!</i>\n\n📄 {} {}({}):\n👨‍⚕️ Шақырдыңыз: <b>{} адам</b>".format(bot_username, str(message.chat.id), str(message.from_user.first_name), str(message.from_user.last_name), str(message.chat.id), libs.getCountOfReffereds(message.chat.id)))
    elif message.text == '👤 Авторы':
        response = libs.getAuthors(1)
        await message.answer(response[0], reply_markup=response[1])
    elif message.text == '-📊-':
        if libs.isAdmin(message.chat.id):
            await message.answer(libs.getStats())
    elif message.text == '✅ Подписаться':
        await message.answer('<b>Поздравляю</b> 🥳\nТеперь каждый день будете получать произведение\n\n<i>Для отписки:</i> /unsubscribe')
    else:
        await message.answer('<i>{}</i>'.format(message.text), reply_markup=kb.typeButton)




@dp.callback_query_handler(lambda c: c.data and c.data.startswith('fromauthors'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    response = libs.searchPoem(1, "- "+callback_query.message.text )
    await bot.edit_message_text(response[0], callback_query.from_user.id, callback_query.message.message_id, reply_markup=response[1])

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('frompoems'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    response = libs.searchPoem(1, callback_query.message.text)
    await bot.edit_message_text(response[0], callback_query.from_user.id, callback_query.message.message_id, reply_markup=response[1])

@dp.callback_query_handler(lambda c: c.data and c.data== 'random')
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    poem = libs.getRandomPoem(); keyboard = kb.getPdfButton(poem[0], True)
    await bot.send_message(callback_query.from_user.id, "<b>{}</b>\n<i>{}</i>\n\n{}\n\nДругие произведение автора: /a{}".format(poem[1], poem[2], poem[3], poem[0]), reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('pdf'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    poem_id = callback_query.data.split('|')[1]
    await bot.send_chat_action(callback_query.from_user.id, "upload_document")
    poem = libs.getNativePoem(poem_id)
    file = libs.getPdfOfPoem(callback_query.from_user.id, poem[1], poem[2], poem[3])
    await bot.send_document(callback_query.from_user.id, InputFile('fonts/'+file, poem[1]+'.pdf') )
    libs.deleteFile('fonts/'+file)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('author'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    response = libs.getAuthors(int(callback_query.data.split('|')[1]))
    await bot.edit_message_text(response[0], callback_query.from_user.id, callback_query.message.message_id, reply_markup=response[1])
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('poem'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    response = libs.searchPoem(int(callback_query.data.split('|')[1]), callback_query.message.text)
    await bot.edit_message_text(response[0], callback_query.from_user.id, callback_query.message.message_id, reply_markup=response[1])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





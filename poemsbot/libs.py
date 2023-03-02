import sqlite3
import math
import keyboards as kb
from datetime import datetime
from fpdf import FPDF
import os
import random

usersdb = sqlite3.connect('users.db'); users = usersdb.cursor()
poemdb = sqlite3.connect('poems.db'); poems = poemdb.cursor()

def newUser(uid, fname, lname, uname, ref):
	dtime = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
	users.execute("INSERT OR IGNORE INTO users VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '0', '{}')".format(uid, fname, lname, uname, dtime, ref))
	usersdb.commit()
def isAdmin(uid):
	users.execute("SELECT * from users WHERE userid = '{}' LIMIT 1".format(uid));
	return users.fetchone()[6]
def getRandomPoem():
	random_poem = poems.execute('SELECT * FROM poems ORDER BY RANDOM() LIMIT 1').fetchone()
	return random_poem
def getCountOfReffereds(uid):
	users.execute("SELECT COUNT(*) from users WHERE refered_from = "+str(uid));
	return str(users.fetchone()[0])
def getStats():
	ref = users.execute("SELECT COUNT(*) from users WHERE refered_from != 0").fetchone()[0]
	count = users.execute("SELECT COUNT(*) from users").fetchone()[0]
	lasthour = users.execute("SELECT COUNT(*) from users WHERE datetime(`date`) >= datetime('now','-1 hours')").fetchone()[0]
	last24hour = users.execute("SELECT COUNT(*) from users WHERE datetime(`date`) >= datetime('now','-24 hours')").fetchone()[0]
	today = users.execute("SELECT COUNT(*) FROM 'users' WHERE datetime(`date`) >= datetime('now','start of day')").fetchone()[0]
	thisweek = users.execute("SELECT COUNT(*) from users WHERE datetime(`date`) >= datetime('now', 'weekday 0', '-7 days')").fetchone()[0]
	thismonth = users.execute("SELECT COUNT(*) from users WHERE datetime(`date`) >= datetime('now', 'start of month')").fetchone()[0]
	last3month = users.execute("SELECT COUNT(*) from users WHERE datetime(`date`) >= datetime('now', '-3 months')").fetchone()[0]

	return "<b>🤵 Барлығы:</b> <i>"+str(count)+" адам</i>\n<b>👨‍💼 Рефералкамен кіргендер:</b> <i>"+str(ref)+" адам</i>\n\n<b>- 1 сағат:</b> <i>"+str(lasthour)+" адам</i>\n<b>- 24 сағат:</b> <i>"+str(last24hour)+" адам</i>\n<b>- Бүгін:</b> <i>"+str(today)+" адам</i>\n<b>- Осы апта:</b> <i>"+str(thisweek)+" адам</i>\n<b>- Осы ай:</b> <i>"+str(thismonth)+" адам</i>\n<b>- 3 айда:</b> <i>"+str(last3month)+" адам</i>";
def getAuthor(id):
	return poems.execute("SELECT author, COUNT(*) as c FROM poems WHERE author = (SELECT author FROM poems WHERE id = '{}' LIMIT 1) LIMIT 1".format(id)).fetchone()
def getAuthors(page):
	perpage = 35
	maxpage = math.ceil(poems.execute("SELECT COUNT(*) FROM(SELECT COUNT(*) from poems GROUP BY author)").fetchone()[0]/perpage)
	pp = perpage+1; mp = perpage-1; offset = (page-1)*perpage;

	answer = "<i>Авторы:</i>\n"

	authors = poems.execute("SELECT id, author, COUNT(*) as c FROM poems GROUP BY author ORDER BY COUNT(*) DESC LIMIT {}, {}".format(offset, pp)).fetchall()
	count = len(authors)
	key = 0
	for author in authors:
		answer += "\n/a{} <b>{}</b> <i>({})</i>".format(author[0], author[1], author[2])
		if key == mp:
			break
		key += 1
	return [answer, kb.pageination('author', page, maxpage, perpage, count)]
def searchPoem(page, query, showAuthorInfo = False):
	query = query.splitlines()[0]
	perpage = 10
	pp = perpage+1; mp = perpage-1; offset = (page-1)*perpage;
	if len(query)>45:
		return ['😲 Тым ұзын', None]

	answer = "<i>"+str(query)+"</i>";
	if query == '---':
		maxpage = math.ceil(poems.execute("SELECT COUNT(*) from poems").fetchone()[0]/perpage)
		response = poems.execute("SELECT * from poems LIMIT {}, {}".format(offset, pp)).fetchall()
	elif query.startswith('-- '): 
		maxpage = math.ceil(poems.execute("SELECT COUNT(*) as c FROM poems WHERE author = '{}'".format(query[3:])).fetchone()[0]/perpage)
		response = poems.execute("SELECT * from poems WHERE author = '{}' LIMIT {}, {}".format(query[3:], offset, pp)).fetchall()
	elif query.startswith('- '):
		maxpage = math.ceil(poems.execute("SELECT COUNT(*) as c FROM poems WHERE author LIKE '%{}%'".format(query[2:])).fetchone()[0]/perpage)
		response = poems.execute("SELECT * from poems WHERE author LIKE '%{}%' LIMIT {}, {}".format(query[2:], offset, pp)).fetchall()
	else:
		maxpage = math.ceil(poems.execute("SELECT COUNT(*) from poems WHERE name LIKE '%{0}%'".format(query)).fetchone()[0]/perpage)
		response = poems.execute("SELECT id, name, author from poems WHERE name LIKE '%{0}%' \
        ORDER BY(CASE WHEN name = '{0}' THEN 1 WHEN name LIKE '{0}%' THEN 2 ELSE 3 END), name \
        LIMIT {1}, {2}".format(query, offset, pp)).fetchall()
	count = len(response)
	if count == 0:
		return ['<i>{}</i>\n😔 Табылмады!\n\n<i>• Бас әріппен жазып көріңіз немесе барлығын кіші әріппен, ҚАТЕСІЗ\n• Адам аттарын бас әріппен\n• Қазақша шрифтпен\n• Егер табылмаса тек бір-екі сөзбен іздеңіз\n\nӨлең қосу бойынша: /contact</i>'.format(query), None]
	key = 0
	for poem in response:
		answer += "\n-------------------------\n/o{} <b>{}</b> — <i>{}</i>".format(poem[0], poem[1], poem[2])
		if key == mp:
			break
		key += 1
	if showAuthorInfo:
		return [answer, kb.pageination('poem', page, maxpage, perpage, count, query[3:])]
	else:
		return [answer, kb.pageination('poem', page, maxpage, perpage, count, False)]
def addPoem(name, author, content, id_insite='0'):
	if issetPoem(content):
		return False
	poems.execute("INSERT into poems values (NULL, '{}', '{}', '{}', '{}')".format(name, author, content, id_insite))
	poemdb.commit()
def issetPoem(content):
	poem =  poems.execute("SELECT * from poems WHERE content = '{}' LIMIT 1".format(content)).fetchone()
	if poem is None:
		return False
	return True
def getPoem(id): 
	poem = poems.execute("SELECT * from poems WHERE id = {} LIMIT 1".format(id)).fetchone()
	return "<b>{}</b>\n<i>{}</i>\n\n{}\n\nДругие произведение автора: /a{}".format(poem[1], poem[2], poem[3], poem[0])
def deletePoem(id):
	poems.execute("DELETE from poems where id = {}".format(id))
	poemdb.commit()
	return True
def getUsers():
	return users.execute("SELECT userid FROM users").fetchall()
def getAdmins():
	return users.execute("SELECT userid FROM users WHERE admin = '1'").fetchall()
def getNativePoem(id):
	return poems.execute("SELECT * from poems WHERE id = {} LIMIT 1".format(id)).fetchone()
def getPdfOfPoem(userid, title, author, poem):
	pdf = FPDF()
	pdf.add_page()

	pdf.add_font('KZ Arial', '', 'fonts/KZ Arial.ttf', uni=True)
	pdf.add_font('KZ Arial Bold', '', 'fonts/KZ Arial Bold.ttf', uni=True)
	pdf.add_font('KZ Arial Italic', '', 'fonts/KZ Arial Italic.ttf', uni=True)

	pdf.set_font('KZ Arial Bold', '', 12)
	pdf.multi_cell(200, 5, txt = title, align = 'C')

	pdf.set_font('KZ Arial Italic', '', 9)
	pdf.multi_cell(200, 5, txt = "Авторы: {}".format(author), align = 'C')

	pdf.set_font('KZ Arial', '', 9)
	pdf.multi_cell(200, 5, txt = poem, align = 'C')
	file = "{}_{}.pdf".format(userid, random.randint(1, 1000000))
	pdf.output("fonts/"+file)   
	return file
def deleteFile(path):
	os.remove(path)
def removeUser(id):
	users.execute("DELETE from users where userid = {}".format(id))
	usersdb.commit()
	return True
def usersVacuum():
	users.execute("VACUUM")
	return True


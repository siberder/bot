import jsonpickle
import datetime
from weasyprint import HTML
from yattag import Doc


class WishDayHours:
	anyhours = ["Any", "any"]
	off = ["OFF", "off"]

	def checkAny(text):
		return len([x for x in text.split() if x.lower() in WishDayHours.anyhours]) > 0

	def checkOff(text):
		return len([x for x in text.split() if x.lower() in WishDayHours.off]) > 0

class WishDay:
	startHour = None
	endHour = None

	def __init__(self, startHour = None, endHour = None):
		self.startHour = startHour
		self.endHour = endHour

	def __str__(self):
		return "{0} - {1}".format(self.startHour, self.endHour)

class Wish:
	def __init__(self):
		self.name = "Unnamed"
		self.uid = -1
		self.weekStart = datetime.date.today()
		self.days = []
		self.comment = ""

	def __str__(self):
		pstr = "Пожелания от {0} с {1:%Y-%m-%d} по {2:%Y-%m-%d}\n".format(self.name, self.weekStart, self.weekStart + datetime.timedelta(days = 7))
		
		for i, day in enumerate(self.days):
			pstr += "[{0:%Y-%m-%d}] {1}\n".format(self.weekStart + datetime.timedelta(days = i), day)

		pstr += "\nКомментарий:\n" + self.comment if self.comment else ""
		return pstr		

def loadWishes(path):
	try:
		with open(path, "r") as f:
			wsh = jsonpickle.decode(f.read())
			print(str(len(wsh)) + " wishes loaded")
			return wsh
	except Exception as e:
		if e == FileNotFoundError:
			open(path, 'w+')

		return []

def saveWishes(path, wishes):
	try:
		with open(path, "w") as f:
			f.write(jsonpickle.encode(wishes))
	except Exception as e:
		if e == FileNotFoundError:
			open(path, 'w+')

def getNextTue():
	curdate = datetime.date.today()
	return curdate + datetime.timedelta(days = 7 - curdate.weekday() + 1) # Max days in week - current day in week + tuesday number

def getCurTue():
	curdate = datetime.date.today()	
	return curdate + datetime.timedelta(days = - curdate.weekday() + 1) # Max days in week - current day in week + tuesday number

def getDayHoursFromString(text):
	hours = text.strip(" ").split("-")

	day = WishDay()

	if len(hours) > 1:
		if WishDayHours.checkAny(hours[0]):
			day.startHour = WishDayHours.anyhours[0]
		else:
			day.startHour = hours[0]

		if WishDayHours.checkAny(hours[1]):
			day.endHour = WishDayHours.anyhours[0]
		else:
			day.endHour = hours[1]
	elif WishDayHours.checkAny(text):
		day.startHour = WishDayHours.anyhours[0]
		day.endHour = WishDayHours.anyhours[0]
	elif WishDayHours.checkOff(text):
		day.startHour = WishDayHours.off[0]
		day.endHour = WishDayHours.off[0]

	return day

def getWishDaysFromText(text):
	text = [x.strip("\n") for x in text.split("\n")]

	nextWeekWords = ["на следующую", "на след", "след", "следующую"]
	isNextWeek = len([x for x in text[0].split() if x.lower() in nextWeekWords]) > 0

	wish = Wish()
	wish.weekStart = getNextTue() if isNextWeek else getCurTue()

	i = 1
	d = 0
	while i < len(text) and d < 7:
		if text[i]:	
			wish.days.append(getDayHoursFromString(text[i]))		
			d += 1

		i += 1

	wish.comment = "\n".join(text[i:])

	return wish 

def getTestWish():
	with open("ws", "r", encoding="utf-8") as f:
		return f.read()

def addWish(name, uid, text):
	print("Adding wish of {0} ({1})".format(name, str(uid)))

	wish = getWishDaysFromText(text)
	wish.name = name
	wish.uid = uid
	
	wishes.append(wish)
	saveWishes(wishPath, wishes)

	return wish

def getWishes(uid = -1, weekStart = None):
	if weekStart is None:
		weekStart = getCurTue()

	filtered = [x for x in wishes if x.weekStart == weekStart]

	if uid > 0:
		filtered = [x for x in filtered if x.uid == uid]

	return filtered

def addFakeWishes(count):
	print("Adding %s fake wishes" % count)

	for x in range(0, count):
		addWish("Name Surname", count, getTestWish())

def generateWishesHTML(wsh):
	print("Generating wishes HTML..")

	doc, tag, text = Doc().tagtext()

	doc.asis('<!DOCTYPE html>')

	with tag('head'):
		doc.asis('<meta charset=utf-8>')

	with tag('body'):
		with tag('h1'):
			text("Пожелания")

		with tag('table'):
			with tag('tr'):
				headrows = ["Имя", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Понедельник", "Комментарий"]

				for hrow in headrows:
					with tag('th'):
						text(hrow)

			with tag("tr"):
				pass

			for w in wsh:
				with tag("tr"):
					with tag("td"):
						text(w.name)

					for x in range(0, 7):
						daysInWish = len(w.days)

						with tag("td"):
							if x < daysInWish and w.days[x] is not None:
								text(str(w.days[x]))

					with tag("td"):
						text(w.comment)

	rdyDoc = doc.getvalue()

	with open("lastwishes.html", "w+") as f:
		f.write(rdyDoc)

	return rdyDoc	

def getWishesHTMLFile():
	try:
		return open("wishes.html", "rb")
	except FileNotFoundError:
		generateWishesHTML(wishes)
		getWishesHTMLFile()

def generateWishesPDF(htmlstring):
	print("Generating wishes PDF..")

	path = 'wishes.pdf'
	# pdfkit.from_string(htmlstring, path) 
	HTML(string=htmlstring).write_pdf(path)
	return open(path, "rb")

def getWishesPDFFile():
	try:
		return open("wishes.pdf", "rb")
	except FileNotFoundError:
		generateWishesPDF(getWishesHTMLFile())
		getWishesPDFFile()

def getWishesReport(wishes):
	print("Getting wishes report..")

	try:
		html = generateWishesHTML(wishes)

		pdfRB = generateWishesPDF(html)
		return pdfRB
	except:
		return getWishesPDFFile()
	

wishPath = "wishes.json"

wishes = loadWishes(wishPath)

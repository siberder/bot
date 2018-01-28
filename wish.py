import jsonpickle
import datetime
import settings
import utils

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
	date = None

	def __init__(self, startHour = None, endHour = None, date = None, text = None):
		self.startHour = startHour
		self.endHour = endHour
		self.date = date

		if text is not None:
			self.setHoursFromString(text) 

	def __str__(self):
		if self.startHour is None or self.endHour is None:
			return "Ошибка в записи"

		if self.startHour == self.endHour:
			return(self.startHour)

		return "{0} - {1}".format(self.startHour, self.endHour)

	def setHoursFromString(self, text):
		hours = text.strip(" ").split("-")

		if len(hours) > 1:
			if WishDayHours.checkAny(hours[0]):
				self.startHour = WishDayHours.anyhours[0]
			else:
				self.startHour = hours[0]

			if WishDayHours.checkAny(hours[1]):
				self.endHour = WishDayHours.anyhours[0]
			else:
				self.endHour = hours[1]
		elif WishDayHours.checkAny(text):
			self.startHour = WishDayHours.anyhours[0]
			self.endHour = WishDayHours.anyhours[0]
		elif WishDayHours.checkOff(text):
			self.startHour = WishDayHours.off[0]
			self.endHour = WishDayHours.off[0]

class Wish:
	def __init__(self, name = "Unnamed", uid = -1, weekStart = None, text = None):
		self.name = name
		self.uid = uid
		self.days = []
		self.comment = ""

		self.setWeekStart(weekStart, text)

		if text is not None:
			self.setFromText(text) 

	def __str__(self):
		pstr = "Пожелания от {0} с {1:%Y-%m-%d} по {2:%Y-%m-%d}\n".format(self.name, self.weekStart, self.weekStart + datetime.timedelta(days = 7))
		
		for i, day in enumerate(self.days):
			pstr += "[{0:%Y-%m-%d}] {1}\n".format(self.weekStart + datetime.timedelta(days = i), day)

		pstr += "\nКомментарий:\n" + self.comment if self.comment else ""
		return pstr	

	def setWeekStart(self, date, text):
		if date is not None:
			self.weekStart = date
			return

		text = [x.strip("\n") for x in text.split("\n")]		

		self.weekStart = utils.getDateFromText(text[0])
		if self.weekStart is None:
			self.weekStart = utils.getCurTue()

	def setFromText(self, text):
		text = [x.strip("\n") for x in text.split("\n")]		

		i = 1
		d = 0
		while i < len(text) and d < 7:
			if text[i]:	
				self.days.append(WishDay(text = text[i]))		
				d += 1

			i += 1

		self.comment = "\n".join(text[i:])

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

def addWish(name, uid, text, date):
	print("Adding wish of {0} ({1})".format(name, str(uid)))

	wish = Wish(name, uid, date, text)
	
	isOverwritten = False
	matches = [w for w in wishes if w.uid == uid and w.weekStart == date]
	if len(matches) > 0:
		isOverwritten = True
		wishes[wishes.index(matches[0])] = wish
	else:
		wishes.append(wish)

	saveWishes(wishPath, wishes)

	return wish, isOverwritten

def getTestWish():
	with open("ws", "r", encoding="utf-8") as f:
		return f.read()

def addFakeWishes(count):
	print("Adding %s fake wishes" % count)

	for x in range(0, count):
		addWish("Name Surname", count, getTestWish())	

wishPath = "wishes.json"

wishes = loadWishes(wishPath)
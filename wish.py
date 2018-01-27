import jsonpickle
import datetime
import settings

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
			setHoursFromString(text) 

	def __str__(self):
		if self.startHour is None or self.endHour is None:
			return "Ошибка в записи"

		if self.startHour == self.endHour:
			return(self.startHour)

		return "{0} - {1}".format(self.startHour, self.endHour)

	def setHoursFromString(self, text):
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
	curTue = getCurTue()
	return curTue + datetime.timedelta(days = 7 - curTue.weekday()  + settings.wishesStartWeekday) # days in week - current day in week + tuesday

def getCurTue():
	curdate = datetime.date.today()

	# If we are above wed, we have to leave wishes to next week
	if curdate.weekday() > settings.wishesDeadlineWeekday:
		curdate += datetime.timedelta(days = 7)

	return getExactWeekStart(curdate)

def getExactWeekStart(curdate):
	return curdate + datetime.timedelta(days = - curdate.weekday() + settings.wishesStartWeekday) # days in week - current day in week + tuesday

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

wishPath = "wishes.json"

wishes = loadWishes(wishPath)

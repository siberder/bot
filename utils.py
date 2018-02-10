import re
import settings
from datetime import datetime, date, timedelta

def getDateFromText(text):
	try:
		isNextWeek = (checkWordsInText(text, settings.nextWeekWords) is not None)

		if isNextWeek:
			return getNextTue()

		datere = re.compile(r'\d+[./:-]\d+[./:-]\d+')
		matches = datere.findall(text)[0]

		matches = re.sub(r"[./:-]", ".", matches)

		date = datetime.strptime(matches, "%d.%m.%Y")

		#date = date.strftime("%d.%m.%Y")

		return date.date()
	except Exception as e:
		print(e)

		return None

def checkWordsInText(text, words):
	# Lower all words
	textlines = text.split("\n")
	textfrags = []
	[textfrags.extend(l.split(" ")) for l in textlines]
	text = [w.lower() for w in textfrags]
	words = [w.lower() for w in words]

	for w in words:
		if w in text:
			return w

	return None

# Gets next wish day
def getNextTue():
	curTue = getCurTue()
	return curTue + timedelta(days = 7 - curTue.weekday()  + settings.wishesStartWeekday) # days in week - current day in week + tuesday

# Gets current wish day
def getCurTue():
	curdate = date.today()

	# If we are above wed, we have to leave wishes to next week
	if curdate.weekday() < settings.wishesDeadlineWeekday:
		curdate += timedelta(days = 7)
	else:
		curdate += timedelta(days = 14)

	return getExactWeekStart(curdate)

# Gets current week start of the date
def getExactWeekStart(curdate):
	date = curdate + timedelta(days = - curdate.weekday() + settings.wishesStartWeekday)
	return date # days in week - current day in week + tuesday

def getCurDatetimeString():
	return datetime.now().strftime("%d.%m.%Y %H:%M:%S")
import command_system
import wish
import wishreporter
import vkapi
import re
from datetime import datetime

def getWishes(uid, body):
	wishesDate = getDateFromText(body)
	curWishes = wish.getWishes(weekStart = wishesDate)

	message = 'Текущие пожелания: '
	message += str(len(curWishes))

	message += "\nДата начала рабочей недели: "
	if wishesDate is not None:
		message += str(wishesDate)
	else:
		message += str(wish.getCurTue().strptime(matches, "%d.%m.%Y"))	

	wishesDoc = wishreporter.getWishesReport(curWishes)

	attachment = ''

	if wishesDoc is None:
		message += "\nЧто-то пошло не так, и документ с пожеланиями не сохранился. Спросите у Влада. Или Господа-бога. Хотя какая разница."
	else:
		attachment = vkapi.upload_document(uid, wishesDoc)

	return message, attachment

def getDateFromText(text):
	try:
		datere = re.compile(r'\d+[./:-]\d+[./:-]\d+')
		matches = datere.findall(text)[0]

		matches = re.sub(r"[./:-]", ".", matches)

		print(matches)
		date = datetime.strptime(matches, "%d.%m.%Y")

		return date
	except Exception as e:
		print(e)

		return None


command = command_system.Command()

command.keys = ['все', 'покажи']
command.description = 'Покажу пожелания'
command.process = getWishes
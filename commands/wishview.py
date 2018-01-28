import command_system
import wish
import wishreporter
import vkapi
import utils
from datetime import datetime

wishesWords = ["пожелания"]
leftsWords = ["неоставивших"]

def showCommandOptionsText():
	msgstr = "Что показывать? Варианты:\n"
	msgstr += command.keys[0] + " " + wishesWords[0] + "\n"
	msgstr += command.keys[0] + " " + leftsWords[0] + "\n"

	return msgstr

def getWishes(uid, body):
	foundWishesWords = (utils.checkWordsInText(body, wishesWords) is not None)
	foundLeftsWords = (utils.checkWordsInText(body, leftsWords) is not None)

	if foundWishesWords is False and foundLeftsWords is False:
		return showCommandOptionsText(), ''

	wishesDate = utils.getDateFromText(body)

	if foundWishesWords:
		curWishes = wish.getWishes(weekStart = wishesDate)

		wishCount = len(curWishes)
		if wishCount == 0:
			return "Пожеланий нет.", ''

		message = 'Оставлено пожеланий: ' + str(wishCount)

		message += "\nДата начала рабочей недели: "
		if wishesDate is not None:
			message += str(wishesDate)
		else:
			message += str(utils.getCurTue().strftime("%d.%m.%Y"))	

		wishesDoc = wishreporter.getWishesReport(curWishes)

		attachment = ''

		if wishesDoc is None:
			message += "\nЧто-то пошло не так, и документ с пожеланиями не сохранился. Спросите у Влада. Или Господа-бога. Хотя какая разница."
		else:
			attachment = vkapi.upload_document(uid, wishesDoc)

		return message, attachment

	return 'Ошибка', ''

command = command_system.Command()

command.keys = ['покажи', 'показать']
command.description = 'Покажу пожелания'
command.process = getWishes
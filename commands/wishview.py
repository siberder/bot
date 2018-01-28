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
	if wishesDate is None:
		wishesDate = utils.getCurTue()

	if foundWishesWords:
		wreport = wishreporter.getWishesReport(wish.wishes, wishreporter.WishFilterSettings(date = wishesDate))

		wishCount = len(wreport.wishes)
		if wishCount == 0:
			return "Пожеланий нет.", ''

		message = 'Оставлено пожеланий: ' + str(wishCount)

		message += "\nДата начала рабочей недели: "
		if wreport.date is not None:
			message += str(wreport.getDateStr())
		else:
			message += str(utils.getCurTue().strftime("%d.%m.%Y"))	

		wishesDoc = wreport.reportPDF()

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
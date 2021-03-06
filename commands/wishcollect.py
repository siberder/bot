import command_system
import wish
import vkapi
import utils

def addWish(uid, body):
	name = vkapi.getName(uid)   
	date = utils.getDateFromText(body)
	newWish, isOverwritten = wish.addWish(name, uid, body, date)

	message = "Твои пожелания записаны :)\n" if isOverwritten is False else "Твои пожелания перезаписаны :)\n"
	message += str(newWish)

	return message, ''

command = command_system.Command()

command.keys = ['пожелания', 'пожелания\n', 'пожелашки']
command.description = 'Запишу твои пожелания'
command.process = addWish
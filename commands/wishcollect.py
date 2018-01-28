import command_system
import wish
import vkapi

def addWish(uid, body):
	name = vkapi.getName(uid)   
	newWish, isOverwritten = wish.addWish(name, uid, body)

	message = "Твои пожелания записаны :)\n" if isOverwritten is False else "Твои пожелания перезаписаны :)\n"
	message += str(newWish)

	return message, ''

command = command_system.Command()

command.keys = ['пожелания', 'пожелания\n', 'пожелашки']
command.description = 'Запишу твои пожелания'
command.process = addWish
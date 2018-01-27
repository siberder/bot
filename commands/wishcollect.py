import command_system
import wish
import vkapi

def addWish(uid, body):
	name = vkapi.getName(uid)   
	newWish = wish.addWish(name, uid, body)

	message = "Твои пожелания записаны :)\n" + str(newWish)

	return message, ''

command = command_system.Command()

command.keys = ['пожелания', 'пожелания\n', 'пожелашки']
command.description = 'Запишу твои пожелания'
command.process = addWish
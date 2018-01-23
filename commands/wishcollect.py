import command_system
import wish
import vkapi

def addWish(uid, body):
	name = vkapi.getName(uid)   
	message = wish.addWish(name, uid, body)

	if message is 1:
		message = "Твои пожелания записаны :)"

	return message, ''

cat_command = command_system.Command()

cat_command.keys = ['пожелания', 'пожелашки']
cat_command.description = 'Запишу твои пожелания'
cat_command.process = addWish
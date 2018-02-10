import command_system
import wishreminder
import settings

def remind(uid, body):
	if uid not in settings.ignoreids:
		return "Вы не администратор, чтобы вызывать эту функцию", ""

	wishreminder.remindWishes()
	return "Напомнил", ''

command = command_system.Command()

command.keys = ['напомни']
command.description = 'Напомню всем кто не оставил пожелания, оставить их'
command.process = remind
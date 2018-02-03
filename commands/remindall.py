import command_system
import wishreminder

def remind(uid, body):
	wishreminder.remindWishes()
	return "Напомнил", ''

command = command_system.Command()

command.keys = ['напомни']
command.description = 'Напомню всем кто не оставил пожелания, оставить их'
command.process = remind
import command_system
import vkapi
import settings

def info(uid, body):
	names = vkapi.packIDsToNames(settings.ignoreids)

	msg = "Администраторы бота:"

	for name in names:
		msg += "\n" + name

	return msg, ''


info_command = command_system.Command()

info_command.keys = ['администрация', 'админы', 'менеджеры', 'манагеры']
info_command.description = 'Покажу администраторов бота'
info_command.process = info

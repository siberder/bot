import command_system


def info(uid, body):
    message = ''
    for c in command_system.command_list:
    	if c.showInfo:
        	message += c.keys[0] + ' - ' + c.description + '\n'
    return message, ''


info_command = command_system.Command()

info_command.keys = ['помощь', 'помоги', 'help']
info_command.description = 'Покажу список команд'
info_command.process = info
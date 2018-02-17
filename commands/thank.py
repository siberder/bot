import command_system
import random

def action(uid, body):
	thankSentences = ["Да пожалуйста %)", "На здоровье)", "Не за что :)"]

	return random.choice(thankSentences), ''

command = command_system.Command()


command.keys = ['спасибо', "благодарю", "спасибочко", "благодарствую", "мерси", "удачно", "благодарность"]
command.description = 'Напомню всем кто не оставил пожелания, оставить их'
command.process = action
command.showInfo = False

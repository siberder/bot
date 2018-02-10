token = 'b882cd131dc1e045642e3127169324fe8ddb1eef67ff8a8bbb000cb4a17b5a0bcac50287c8bbbf2e179a3'
confirmation_token = 'f75d26cf'

wishesPath = "wishes.json"

group_id = 52421856
ignoreids = [33351327]
ignoreManagers = True

wishesStartWeekday = 1
wishesDeadlineWeekday = 3

nextWeekWords = ["на следующую", "на след", "след", "следующую"]
# remindMsg = "Please, leave your wishes on {date}! Write them to me, please"
remindMsg = "У тебя не оставлены пожелания на {date}! Напиши их мне, пожалуйста"

dateFromat = ""

def getIgnores():
	print("Getting ignore ids..")
	try:
		import vkapi

		managers = vkapi.getManagers()

		ignoreids = [x['id'] for x in managers if x['role'] is not "editor"]

		print("Ignoring: " + str(ignoreids))

		return ignoreids
	except Exception as e:
		print(e)
		return []

if ignoreManagers:
	ignoreids.extend(getIgnores())
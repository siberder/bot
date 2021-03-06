import wishreporter
import jsonpickle
import vkapi
import settings
import utils
import sys
from datetime import datetime, timedelta

def loadWishes():
	try:
		with open(settings.wishesPath, "r") as f:
			wsh = jsonpickle.decode(f.read())
			print(str(len(wsh)) + " wishes loaded")
			return wsh
	except Exception as e:
		if e == FileNotFoundError:
			open(settings.wishesPath, 'w+')

		print("No wishes loaded")
		print(e)
		return []

def getRemindMembers():
	groupMembers = vkapi.getGroupMembers()
	print("Group members: " + str(groupMembers))

	ignoreMembers = settings.ignoreids
	print("Ignore members: " + str(ignoreMembers))

	resultMembers = list(set(groupMembers) - set(ignoreMembers))
	print("Remind members: " + str(resultMembers))

	return resultMembers

def getUsersWithoutWishes():
	wishes = loadWishes()
	report = wishreporter.getWishesReport(wishes, wishreporter.WishFilterSettings(date = utils.getCurTue()))

	userWithWishes = [u.uid for u in report.wishes]
	print("Users with wishes: " + str(userWithWishes))

	allPeople = getRemindMembers()

	usersWithoutWishes = list(set(allPeople) - set(userWithWishes))
	print("Users without wishes: " + str(usersWithoutWishes))

	print("{0} users found without wishes".format(len(usersWithoutWishes)))

	return usersWithoutWishes

def autoRemindWishes():
	print("Reminding on " + utils.getCurDatetimeString())
	print("Getting users with no current wishes..")
	usersWithoutWishes =  getUsersWithoutWishes()

	print("Reminding to %s people to left wishes." % len(usersWithoutWishes))

	curTue = utils.getCurTue()
	msg = settings.remindMsg.format(date=str(curTue.strftime("%d.%m.%Y")), enddate=str((curTue + timedelta(days = 7)).strftime("%d.%m.%Y")))

	vkapi.send_many_msgs(usersWithoutWishes, settings.token, msg)

	print("Reminded.")

if __name__ == "__main__":
	print(str(sys.argv))

	import os
	os.chdir(os.path.dirname(__file__))
	print("Running at " + str(os.path.dirname(os.path.abspath(__file__))))
	print("Working dir at " + str(os.getcwd()))

	if len(sys.argv) > 1 and sys.argv[1] == "-remind":
		print("Reminding")
		autoRemindWishes()
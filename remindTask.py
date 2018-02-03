import wishreporter
import vkapi
import settings
import utils
import sys

def loadWishes():
	try:
		with open(settings.wishesPath, "r") as f:
			wsh = jsonpickle.decode(f.read())
			print(str(len(wsh)) + " wishes loaded")
			return wsh
	except Exception as e:
		if e == FileNotFoundError:
			open(settings.wishesPath, 'w+')

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

	msg = settings.remindMsg.format(date=str(utils.getCurTue()))

	vkapi.send_many_msgs(usersWithoutWishes, settings.token, msg)

	print("Reminded.")

if __name__ == "__main__":
	print(str(sys.argv))
	if len(sys.argv) > 1 and sys.argv[1] == "-remind":
		print("Reminding")
		autoRemindWishes()
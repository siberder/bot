import wish
import wishreporter
import settings
import vkapi
import schedule
import time
import utils
import threading
import sys

def getRemindMembers():
	groupMembers = vkapi.getGroupMembers()
	print("Group members: " + str(groupMembers))

	ignoreMembers = settings.ignoreids
	print("Ignore members: " + str(ignoreMembers))

	resultMembers = list(set(groupMembers) - set(ignoreMembers))
	print("Remind members: " + str(resultMembers))

	return resultMembers

def getUsersWithoutWishes():
	report = wishreporter.getWishesReport(wish.wishes, wishreporter.WishFilterSettings(date = utils.getCurTue()))

	userWithWishes = [u.uid for u in report.wishes]
	print("Users with wishes: " + str(userWithWishes))

	allPeople = getRemindMembers()

	usersWithoutWishes = list(set(allPeople) - set(userWithWishes))
	print("Users without wishes: " + str(usersWithoutWishes))

	print("{0} users found without wishes".format(len(usersWithoutWishes)))

	return usersWithoutWishes

def remindWishes():
	print("Reminding on " + utils.getCurDatetimeString())
	print("Getting users with no current wishes..")
	usersWithoutWishes =  getUsersWithoutWishes()

	print("Reminding to %s people to left wishes." % len(usersWithoutWishes))

	msg = settings.remindMsg.format(date=str(utils.getCurTue()))

	vkapi.send_many_msgs(usersWithoutWishes, settings.token, msg)

	print("Reminded.")

def startSchedule():
	print("Starting schedule..")
	#schedule.every(1).minutes.do(remindWishes)
	schedule.every().day.at("10:30").do(remindWishes)

	while True:
		print("Schedule checked")
		schedule.run_pending()
		time.sleep(30)
		print("Schedule check end")

if __name__ == "__main__":
	print(str(sys.argv))
	if sys.argv[1] == "-remind":
		print("Reminding")
		remindWishes()
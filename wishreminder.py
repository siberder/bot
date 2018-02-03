import wish
import wishreporter
import settings
import vkapi
import schedule
import time
import utils

def getRemindMembers():
	return list(set(vkapi.getGroupMembers()) - set(settings.ignoreids))

def getUsersWithoutWishes():
	report = wishreporter.getWishesReport(wish.wishes, wishreporter.WishFilterSettings(date = utils.getCurTue()))

	userWithWishes = [u.uid for u in report.wishes]
	allPeople = getRemindMembers()

	usersWithoutWishes = list(set(allPeople) - set(userWithWishes))

	print("{0} users found without wishes".format(len(usersWithoutWishes)))

	return usersWithoutWishes

def remindWishes():
	print("Getting users with no current wishes..")
	usersWithoutWishes =  getUsersWithoutWishes()

	print("Reminding to %s people to left wishes." % len(usersWithoutWishes))

	msg = settings.remindMsg.format(date=str(utils.getCurTue()))

	vkapi.send_many_msgs(usersWithoutWishes, settings.token, msg)

	print("Reminded.")

def startSchedule():
	print("Starting schedule..")
	schedule.every(1).minutes.do(remindWishes)
	#schedule.every().day.at("10:30").do(remindWishes)

	while True:
		schedule.run_pending()
		time.sleep(60)

#startSchedule()
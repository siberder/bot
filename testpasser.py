from login import login
import requests
import random

class EProgram():
	def __init__(self, fullname = None, eid = None, percent = 0):
		self.fullname = fullname
		self.eid = eid
		self.percent = percent

		if fullname is not None:
			self.setFromName(fullname)		

	def setFromName(self, fullname):		
		digits = [int(s) for s in fullname.split() if s.isdigit()]
		if len(digits) > 0:
			self.eid = digits[-1]
			self.name = fullname.replace(" " + str(digits[-1]), "")
		else:
			print("Unable to set from fullname: " + fullname)


def getEducationPageHTML(ses):
	print("Getting education page..")

	if ses is None:
		print("No session!")
		return

	htmlstring = ses.get("http://amspace.eu/education/").text

	with open("dump.html", "w+", encoding="utf-8") as f:
		f.write(htmlstring)

	return htmlstring

def parseEducationPageHTML(html):
	print("Parsing education page..")

	from bs4 import BeautifulSoup

	soup = BeautifulSoup(html, 'html.parser')

	programs = []

	learnBlocks = soup.find_all('div', class_='ep-cont-learning')

	for block in learnBlocks:
		name = block.find("h3").getText()
		percent = int(block.find('span', class_="ep-cont-prcnt").getText().replace("%", ""))

		programs.append(EProgram(fullname=name, percent=percent))

	print("Parsed %s programs" % len(programs))
	return programs

def passTest(ses, eprogram, percent = 10, time = 1200, randomTime = True):
	if ses is None:
		print("Unable to pass test, no session!")
		return

	if randomTime:
		time += random.randint(-time / 2, time)

	print("Passing %s to %s percent with %s seconds " % (eprogram.fullname, percent, time))	

	resp = ses.post("http://amspace.eu/local/templates/ampeople/php/edu/ajax.php",
		data={'ACTION': 'ADD_PROGRESS', 'ID': str(eprogram.eid), 'PROGRESS': str(percent), 'TIME': str(time)}, timeout=3)

	return resp
from weasyprint import HTML, CSS
from yattag import Doc
import datetime

class WishFilterSettings:
	date = None
	uid = -1

	def __init__(self, date = None, uid = -1):
		self.date = date
		self.uid = uid


class WishReport:
	wishes = []
	date = None
	htmlstring = ""

	def __init__(self, allwishes, filter):
		if filter.date is not None:
			self.date = filter.date
			allwishes = [x for x in allwishes if x.weekStart == filter.date]

		if filter.uid > 0:
			allwishes = [x for x in filtered if x.uid == filter.uid]

		self.wishes = allwishes

	def getDateStr(self):
		return self.date.strftime("%d.%m.%Y") if self.date is not None else ""

	def generateWishesHTML(self):
		print("Generating wishes HTML..")

		doc, tag, text = Doc().tagtext()

		doc.asis('<!DOCTYPE html>')

		with tag('head'):
			doc.asis('<meta charset=utf-8>')
			doc.asis('<link rel=stylesheet href="style.css">')

		with tag('body'):
			with tag('h1'):
				text("Пожелания")

			with tag('h3'):
				text(self.getDateStr())

			with tag('table'):
				with tag('tr'):
					with tag('th'):
						text("")

					for x in range(0, 7):
						with tag('th'):
							(self.wishes[0].weekStart + datetime.timedelta(days = x)).strftime("%d.%m.%Y")

					with tag('th'):
						text("")

				with tag('tr'):
					headrows = ["Имя", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Понедельник", "Комментарий"]

					for hrow in headrows:
						with tag('th'):
							text(hrow)

				with tag("tr"):
					pass

				for w in self.wishes:
					with tag("tr"):
						with tag("td"):
							text(w.name)

						for x in range(0, 7):
							daysInWish = len(w.days)

							with tag("td"):
								if x < daysInWish and w.days[x] is not None:
									text(str(w.days[x]))

						with tag("td"):
							text(w.comment)

		self.htmlstring = doc.getvalue()

		with open("wishes{0}.html".format(self.getDateStr()), "w+") as f:
			f.write(self.htmlstring)

		return self.htmlstring

	def generateWishesPDF(self):
		print("Generating wishes PDF, html string length: " + str(len(self.htmlstring)))

		path = 'wishes.pdf'.format(self.getDateStr())
		
		html = HTML(string=self.htmlstring)
		style = CSS(filename='style.css')
		html.write_pdf(path, stylesheets=[style])
		return open(path, "rb")
		# return "itspdf"

	def reportPDF(self):
		print("Generating report PDF..")

		try:
			self.generateWishesHTML()
			return self.generateWishesPDF()
		except Exception as e:
			print(e)
			return None

def getWishesReport(wishes, filter):
	print("Getting wishes report..")

	filteredWishes = WishReport(wishes, filter)

	return filteredWishes
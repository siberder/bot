from weasyprint import HTML, CSS
from yattag import Doc

def getDocumentText(path):
	try:
		with open(path, "r+") as f:
			return f.read()
	except:
		return ""

def generateWishesHTML(wsh):
	print("Generating wishes HTML..")

	doc, tag, text = Doc().tagtext()

	doc.asis('<!DOCTYPE html>')

	with tag('head'):
		doc.asis('<meta charset=utf-8>')
		
		with tag('style'):
			doc.text(getDocumentText("style.css"))

	with tag('body'):
		with tag('h1'):
			text("Пожелания")

		with tag('table'):
			with tag('tr'):
				headrows = ["Имя", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Понедельник", "Комментарий"]

				for hrow in headrows:
					with tag('th'):
						text(hrow)

			with tag("tr"):
				pass

			for w in wsh:
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

	rdyDoc = doc.getvalue()

	with open("lastwishes.html", "w+") as f:
		f.write(rdyDoc)

	return rdyDoc	

def getWishesHTMLFile():
	try:
		return open("wishes.html", "rb")
	except FileNotFoundError:
		generateWishesHTML(wishes)
		getWishesHTMLFile()

def generateWishesPDF(htmlstring):
	print("Generating wishes PDF, html string length: " + str(len(htmlstring)))

	path = 'wishes.pdf'
	
	html = HTML(string=htmlstring)
	css = CSS(filename="style.css")
	html.write_pdf(path, stylesheets=[css])
	return open(path, "rb")

def getWishesPDFFile():
	try:
		return open("wishes.pdf", "rb")
	except FileNotFoundError:
		generateWishesPDF(getWishesHTMLFile())
		getWishesPDFFile()

def getWishesReport(wishes):
	print("Getting wishes report..")

	try:
		html = generateWishesHTML(wishes)

		pdfRB = generateWishesPDF(html)
		return pdfRB
	except:
		return getWishesPDFFile()
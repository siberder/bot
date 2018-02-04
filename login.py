import requests, requests.utils, jsonpickle

email = 'cool.kozhin@yandex.ru'
password = 'PassThatPass'
# email = 'Riforo@mail.ru'
# password = 'QkA4SCn5'
sesPath = "session"

def login(email, password):
	print("Loggin in with {} : {}".format(str(email), str(password)))
	loginData = {'AUTH_FORM': 'Y', 'Login': 'Войти', 'TYPE': 'AUTH', 'USER_LOGIN': email, 'USER_PASSWORD': password, 'USER_REMEMBER': 'N'}
	ses = requests.Session()
	ses.post("http://amspace.eu/?login=yes", data = loginData)

	if "BITRIX_SM_LOGIN" not in ses.cookies:
		print("Failed to log in with {} : {}".format(str(email), str(password)))
		return None

	return ses

def saveSession(path, ses):
	with open(path, 'w') as f:
		f.write(jsonpickle.encode(requests.utils.dict_from_cookiejar(ses.cookies)))

def loadSession(path):
	with open(path, 'r') as f:
		cookies = requests.utils.cookiejar_from_dict(jsonpickle.decode(f.read()))
		s = requests.Session()
		s.cookies = cookies
		return s
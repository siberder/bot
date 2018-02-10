import vk
import random
import requests
import settings
import time

session = vk.Session()
api = vk.API(session, v=5.0)


def get_random_wall_picture(group_id):
    max_num = api.photos.get(owner_id=group_id, album_id='wall', count=0)['count']
    num = random.randint(1, max_num)
    photo = api.photos.get(owner_id=str(group_id), album_id='wall', count=1, offset=num)['items'][0]['id']
    attachment = 'photo' + str(group_id) + '_' + str(photo)
    return attachment

def upload_document(user_id, document):
	url = api.docs.getMessagesUploadServer(access_token=settings.token, type="doc", peer_id=user_id)["upload_url"]

	uploadedFile = requests.post(url, files={"file": document}).json()["file"]
	
	resp = api.docs.save(access_token=settings.token, file=uploadedFile, title="Wishes.pdf")[0]

	print(resp)

	if "error" in resp:
		return ""

	return "doc{0}_{1}".format(resp["owner_id"], resp["id"])


def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def send_many_msgs(user_ids, token, message, attachment=""):
	usercount = len(user_ids)

	maxMsgs = 25
	requestTpl = 'API.messages.send({{"access_token":"{token}", "user_id":"{uid}", "message":"{message}", "v":"5.71"}})'

	script = "return {0};"
	sbody = ""

	response = []
	for i, user in enumerate(user_ids):
		sbody += requestTpl.format(token=token, uid=user, message=message)
		sbody += " +" if i + 1 < usercount else ""

		if i - 1 >= maxMsgs:
			response.append(api.execute(code=script.format(sbody), access_token=token))
			sbody = ""
			time.sleep(0.4)

	print(script.format(sbody))
	response.append(api.execute(code=script.format(sbody), access_token=token))

	print("Response of sending messages:")
	print(response)
	return response

def getName(uid):
	data = api.users.get(user_id=uid, lang="ru")[0]
	return data["first_name"] + " " + data["last_name"]

def packName(uid, name):
	return "@id{0} ({1})".format(uid, name)

def packIDsToNames(uids):
	names = api.users.get(user_ids=uids, access_token=settings.token)
	return [packName(name['id'], name["first_name"] + " " + name["last_name"]) for name in names]

def getGroupMembers(filter = ""):
	return api.groups.getMembers(access_token=settings.token, group_id=settings.group_id, filter=filter)["users"]

def getIgnores():
	print("Getting ignore ids..")
	try:
		managers = getManagers(filter="managers")

		ignoreids = [x['id'] for x in managers if x['role'] is not "editor"]

		print("Ignoring: " + str(ignoreids))

		return ignoreids
	except Exception as e:
		print(e)
		return []

if settings.ignoreManagers:
	settings.ignoreids.extend(getIgnores())
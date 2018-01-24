import vk
import random
import requests
import settings

session = vk.Session(settings.token)
api = vk.API(session, v=5.0)


def get_random_wall_picture(group_id):
    max_num = api.photos.get(owner_id=group_id, album_id='wall', count=0)['count']
    num = random.randint(1, max_num)
    photo = api.photos.get(owner_id=str(group_id), album_id='wall', count=1, offset=num)['items'][0]['id']
    attachment = 'photo' + str(group_id) + '_' + str(photo)
    return attachment

def upload_document(user_id, document):
	url = api.docs.getMessagesUploadServer(type="doc", peer_id=user_id)

	myfile = {"file": ("wishes.html", document)}


	requests.post(url, data=myfile)

def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def getName(uid):
	data = api.users.get(user_id=uid)[0]
	return data["first_name"] + " " + data["last_name"]
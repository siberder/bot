import command_system
import wish
import vkapi

def getWishes(uid, body):
   message = 'Текущие пожелания: '
   message += str(len(wish.wishes))
   #attachment = 'photo' + str(group_id) + '_' + str(photo)
   return message, attachment

cat_command = command_system.Command()

cat_command.keys = ['все']
cat_command.description = 'Покажу пожелания'
cat_command.process = getWishes
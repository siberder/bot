import command_system
import wish
import vkapi

def getWishes(uid, body):
   message = 'Текущие пожелания: '
   message += str(len(wish.wishes))
   wishesDoc = wish.getWishesReport(wish.wishes)
   attachment = vkapi.upload_document(uid, wishesDoc)
   return message, attachment

cat_command = command_system.Command()

cat_command.keys = ['все']
cat_command.description = 'Покажу пожелания'
cat_command.process = getWishes
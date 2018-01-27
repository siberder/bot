import command_system
import wish
import wishreporter
import vkapi

def getWishes(uid, body):
   message = 'Текущие пожелания: '
   message += str(len(wish.wishes))

   wishesDoc = wishreporter.getWishesReport(wish.wishes)

   attachment = ''

   if wishesDoc is None:
   	message += "\nЧто-то пошло не так, и документ с пожеланиями не сохранился. Спросите у Влада. Или Господа-бога. Хотя какая разница."
   else:
   	attachment = vkapi.upload_document(uid, wishesDoc)

   return message, attachment

cat_command = command_system.Command()

cat_command.keys = ['все']
cat_command.description = 'Покажу пожелания'
cat_command.process = getWishes
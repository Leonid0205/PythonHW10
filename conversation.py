from config import TOKEN
import menu 
from operations_contacts import (contact_id, last_name, first_name, telephone, comment, search_in_telphone_directory, change_last_name, change_first_name, change_telelephone, change_comment)            

from telegram import Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

from telegram.ext import Updater, CommandHandler

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, menu.start)],
    states={
        menu.RESPONSE: [MessageHandler(Filters.regex('^(Save contact|Find contact|'
                                                'Show all contacts|'
                                                'Export|Import|'
                                                'Exit)$'), menu.reply_menu)],
        menu.INPUT_LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, last_name)],
        menu.INPUT_FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, first_name)],
        menu.INPUT_PHONE: [MessageHandler(Filters.text & ~Filters.command, telephone)],
        menu.INPUT_COMMENT: [MessageHandler(Filters.text & ~Filters.command, comment)],
        menu.SEARCH: [MessageHandler(Filters.text & ~Filters.command, search_in_telphone_directory)],
        menu.REPLY_SEARCH: [MessageHandler(Filters.regex('^(Change find conditions|Exit to main menu|Exit)'), menu.response_search)],
        menu.ACTION_CHOOSEN_CONTACT: [MessageHandler(Filters.regex('^(Chose contact|Exit to main menu)'), menu.response_chosen_contact)],
        menu.ID_CONTACT_INPUT: [MessageHandler(Filters.text & ~Filters.command, contact_id)],
        menu.ACTION_USER: [MessageHandler(Filters.regex('^(Delete contact|Change contact|Exit to main menu)'), menu.response_action_contact)],
        menu.ACTION_USER_REPLY: [MessageHandler(Filters.regex('^(Last name|First name|Telephone|Comment)'), menu.contact_what_to_change)],
        menu.INPUT_LAST_NAME_ACTION: [MessageHandler(Filters.text & ~Filters.command, change_last_name)],
        menu.INPUT_FIRST_NAME_ACTION: [MessageHandler(Filters.text & ~Filters.command, change_first_name)],
        menu.INPUT_TELEPHONE_ACTION: [MessageHandler(Filters.text & ~Filters.command, change_telelephone)],
        menu.INPUT_COMMENT_ACTION: [MessageHandler(Filters.text & ~Filters.command, change_comment)],
        menu.EXIT_APP: [MessageHandler(Filters.text, menu.cancel)]
    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('cancel', menu.cancel)],

)

# Добавляем обработчик разговоров `conv_handler`
dispatcher.add_handler(conv_handler)

# Запуск бота
print('Server started')
updater.start_polling()
updater.idle()
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackContext
import operations_contacts
import logger
import import_export_feature as imp_exp

SAVE_CONTACT = 'Save contact'
FIND_CONTACT = 'Find contact'
SHOW_ALL_CONTACTS = 'Show all contacts'
EXPORT = 'Export'
IMPORT = 'Import'
EXIT = 'Exit'
CHANGE_CONDITIONS = 'Change find conditions'
CHANGE = 'Change contact'
DELETE = 'Delete contact'
LAST_NAME = 'Last name'
FIRST_NAME = 'First name'
TELEPHONE = 'Telephone'
COMMENT = 'Comment'
CHOSE_CONTACT = 'Chose contact'
EXIT_TO_MENU = 'Exit to main menu'

RESPONSE, EXIT_APP, INPUT_LAST_NAME, SEARCH, ACTION_CHOOSEN_CONTACT, ID_CONTACT_INPUT, \
REPLY_SEARCH, ACTION_USER, ACTION_USER_REPLY, INPUT_LAST_NAME_ACTION, \
INPUT_FIRST_NAME_ACTION, INPUT_TELEPHONE_ACTION, INPUT_COMMENT_ACTION, INPUT_FIRST_NAME, \
INPUT_PHONE, INPUT_COMMENT = range(16)

def start(update, _):
    reply_keyboard = [['Save contact', 'Find contact', 'Show all contacts',],['Export', 'Import', 'Exit']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Telegram "Cantact app" greets you)\n'
        'Who do you want to do?\n'
        '1 - Save contac\n'
        '2 - Find contact\n'
        '3 - Show all contacts\n'
        '4 - Export\n'
        '5 - Import\n'
        'If you wabt to exit simpli preess or type: /cancel',
        reply_markup=markup_key,)
    return RESPONSE

def reply_menu(update, _):
    logger.my_log(update, _, 'User connected')
    reply = update.message.text
    if reply == EXIT:
        logger.my_log(update, CallbackContext, 'User exited.')
        update.message.reply_text('Goodbye my dear friend)')
        return EXIT_APP
    elif reply == SAVE_CONTACT:
        logger.my_log(update, CallbackContext, 'Save contact.')

        update.message.reply_text(f'{update.effective_user.first_name}\n'
                                   'Input a last name of the contact: \n'
                                   ,reply_markup=ReplyKeyboardRemove())
        return INPUT_LAST_NAME
    elif reply == SHOW_ALL_CONTACTS:
        logger.my_log(update, CallbackContext, 'Show all contacts.')
        return operations_contacts.show_all(update, _)

    elif reply == EXPORT:
        logger.my_log(update, CallbackContext, 'Export.')
        return imp_exp.export(update, _)

    elif reply == IMPORT:
        logger.my_log(update, CallbackContext, 'Import.')
        return imp_exp.import_j(update, _)

    elif reply == FIND_CONTACT:
        logger.my_log(update, CallbackContext, 'Find contact.')
        update.message.reply_text(f'{update.effective_user.first_name}\n'
                                   'Input first name, last name, telephone or comment:\n',
                                   reply_markup=ReplyKeyboardRemove())
        return SEARCH

def reply_searchhh(update, _):
    logger.my_log(update, _, 'Change conditions')
    reply_keyboard = [['Change find conditions'], ['Exit to main menu'], ['Exit']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(f'{update.effective_user.first_name}!\n'
                               'Waiting for your response...',
                               reply_markup=markup_key)

    return REPLY_SEARCH

def response_search(update, _):
    reply = update.message.text
    if reply == EXIT:
        logger.my_log(update, CallbackContext, 'User exited.')
        update.message.reply_text('Goodbye my dear friend)',
                                  reply_markup=ReplyKeyboardRemove())
        return EXIT_APP

    if reply == EXIT_TO_MENU:
        logger.my_log(update, CallbackContext, 'User exited main menu.')
        update.message.reply_text('Exiting main menu...',
                                  reply_markup=ReplyKeyboardRemove(),)
        return start(update, _)

    if reply == CHANGE_CONDITIONS:
        logger.my_log(update, CallbackContext, 'Changing conditions.')
        update.message.reply_text('Input first name, last name, telephone or comment:\n',
                                  reply_markup=ReplyKeyboardRemove())
        return SEARCH

def response_chosen_contact(update, _):
    reply = update.message.text
    if reply == EXIT_TO_MENU:
        operations_contacts.search_result = []
        logger.my_log(update, CallbackContext, 'Moving on to main menu.')
        update.message.reply_text('Moving on to main menu...',
                                  reply_markup=ReplyKeyboardRemove())
        return start(update, _)

    if reply == CHOSE_CONTACT:
        update.message.reply_text('Input contact ID:',
                                  reply_markup=ReplyKeyboardRemove())
        return ID_CONTACT_INPUT

def response_action_contact(update, _):
    reply = update.message.text
    if reply == EXIT_TO_MENU:
        operations_contacts.search_result = []
        logger.my_log(update, CallbackContext, 'Moving on to main menu.')
        update.message.reply_text('Moving on to main menu...',
                                  reply_markup=ReplyKeyboardRemove())
        return start(update, _)

    if reply == DELETE:
        operations_contacts.delete_contact(update, _)
        update.message.reply_text('The contact is deleted.')
        return start(update, _)

    if reply == CHANGE:
        reply_keyboard = [['Last name'], ['First name'], ['Telephone'], ['Comment']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(f'{update.effective_user.first_name}!\n'
                                   'Waiting for your response...',reply_markup=markup_key)
        return ACTION_USER_REPLY

def contact_what_to_change(update, _):
    if update.message.text == 'Last name':
        update.message.reply_text('Input last name: ', reply_markup=ReplyKeyboardRemove())
        return INPUT_LAST_NAME_ACTION

    if update.message.text == 'First name':
        update.message.reply_text('Input first name: ', reply_markup=ReplyKeyboardRemove())
        return INPUT_FIRST_NAME_ACTION

    if update.message.text == 'Telephone':
        update.message.reply_text('Input telephone: ', reply_markup=ReplyKeyboardRemove())
        return INPUT_TELEPHONE_ACTION

    if update.message.text == 'Comment':
        update.message.reply_text('Input comment: ', reply_markup=ReplyKeyboardRemove())
        return INPUT_COMMENT_ACTION

def cancel(update, _):
    # определяем пользователя
    # user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    # logger.info("User %s exit the game", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Goodbye my dear friend)', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END
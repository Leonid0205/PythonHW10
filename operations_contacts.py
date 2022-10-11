import json
import logger
import menu
import checks
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler

RESPONSE, EXIT_APP, INPUT_LAST_NAME, SEARCH, ACTION_CHOOSEN_CONTACT, ID_CONTACT_INPUT, \
REPLY_SEARCH, ACTION_USER_REPLY, INPUT_LAST_NAME_ACTION, \
INPUT_FIRST_NAME_ACTION, INPUT_TELEPHONE_ACTION, INPUT_COMMENT_ACTION, INPUT_LAST_NAME, INPUT_FIRST_NAME, \
INPUT_PHONE, INPUT_COMMENT = range(16)

tel_dir = {}
search_result = []
number_condition = 0

def last_name(update, _):
    global tel_dir
    if checks.check_text(update, update.message.text):
        tel_dir['Last name'] = (update.message.text).title()
        update.message.reply_text('Input contact first name: ')
        return INPUT_FIRST_NAME
    else:
        return INPUT_LAST_NAME

def first_name(update, _):
    global tel_dir
    if checks.check_text(update, update.message.text):
        tel_dir['First name'] = (update.message.text).title()
        update.message.reply_text('Input contact telephone name: ')
        return INPUT_PHONE
    else:
        return INPUT_FIRST_NAME

def telephone(update, _):
    global tel_dir
    if checks.check_text(update, update.message.text):
        tel_dir['Telephone'] = (update.message.text).title()
        update.message.reply_text('Input contact comment: ')
        return INPUT_COMMENT
    else:
        return INPUT_PHONE

def comment(update, _):
    global tel_dir
    if checks.check_text(update, update.message.text):
        tel_dir['Comment'] = (update.message.text).title()
        read_or_write_condition(tel_dir, 'rw')
        update.message.reply_text('Contact successfully')
        return menu.start(update, _)
    else:
        return INPUT_COMMENT

def read_or_write_condition(tel_dir, arg):
    if arg == 'rw':
        try:
            with open('telephone_directory.json', 'r') as t_d:
                telephone_dir = json.load(t_d)
        except:
            telephone_dir = []

        telephone_dir.append(tel_dir)
        with open('telephone_directory.json', 'w') as t_d:
            json.dump(telephone_dir, t_d, indent=2,ensure_ascii=False)

    elif arg == 'r':
        try:
            with open('telephone_directory.json', 'r') as t_d:
                telephone_dir = json.load(t_d)
        except:
            telephone_dir = []
        return telephone_dir

def read_or_write_change(text,arg):
    global number_condition
    global search_result
    with open('telephone_directory.json', 'r') as t_d:
        telephone_dir = json.load(t_d)
    temp_num = telephone_dir.index(search_result[number_condition - 1])
    telephone_dir[temp_num][arg] = text
    with open('telephone_directory.json', 'w') as t_d:
        json.dump(telephone_dir, t_d, indent=2, ensure_ascii=False)

def show_all(update, _):
    logger.my_log(update, _, 'Show all contacts.')
    telephone_dir = read_or_write_condition(tel_dir, 'r')
    if len(telephone_dir) == 0:
        update.message.reply_text('The telephone dictionary is empty.')
        return menu.start(update, _)
    update.message.reply_text('The following contacts are found: ')
    for id, i in enumerate(telephone_dir):
        update.message.reply_text(f'Contact ID : {id + 1} \n'
                                  f'Last name: {i["Last name"]}\n'
                                  f'First name: {i["First name"]}\n'
                                  f'Telephone: {i["Telephone"]}\n'
                                  f'Comment: {i["Comment"]}\n')
    return menu.start(update, _)

def search_in_telphone_directory(update, _):
    global search_result
    logger.my_log(update, _, 'Contacts search')
    telephone_dir = read_or_write_condition(tel_dir, 'r')
    if not (update.message.text).isnumeric():
        for i in telephone_dir:
            if update.message.text in i['Last name'] or update.message.text in i['First name'] :
                search_result.append(i)
    else:
        for i in telephone_dir:
            if update.message.text in i['Telephone']:
                search_result.append(i)
    if len(search_result) == 0:
        update.message.reply_text('Nothing found.')
        return menu.reply_searchhh(update, _)
    update.message.reply_text(f'Found {len(search_result)} contacts: ')
    for id, i in enumerate(search_result):
        update.message.reply_text(f'Contact ID: {id + 1} \n'
                                  f'Last name: {i["Last name"]}\n'
                                  f'First name: {i["First name"]}\n'
                                  f'Telephone: {i["Telephone"]}\n'
                                  f'Comment: {i["Comment"]}\n')
    reply_keyboard = [[menu.CHOSE_CONTACT], [menu.EXIT_TO_MENU]]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(f'{update.effective_user.first_name}!\n'
                               'Waiting for your response...',
                               reply_markup=markup_key)

    return ACTION_CHOOSEN_CONTACT

def contact_id(update, _):
    global search_result
    global number_condition
    if checks.check_choose_contact(update, update.message.text):
        number_condition = int(update.message.text)
        if number_condition < 1 or number_condition > len(search_result):
            update.message.reply_text('Input is out of contacts range.')
            return ID_CONTACT_INPUT
        update.message.reply_text(f'Chosen contact ID: {number_condition}')
        update.message.reply_text(f'Last name: {search_result[number_condition - 1]["Last name"]}\n'
                                  f'First name: {search_result[number_condition - 1]["First name"]}\n'
                                  f'Telephone: {search_result[number_condition - 1]["Telephone"]}\n'
                                  f'Comment: {search_result[number_condition - 1]["Comment"]}\n')
        reply_keyboard = [[menu.DELETE], [menu.CHANGE], [menu.EXIT_TO_MENU]]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(f'{update.effective_user.first_name}!\n'
                                   'What do you ewant to do?',
                                   reply_markup=markup_key)
        return ACTION_USER_REPLY
    else:
        return ID_CONTACT_INPUT

def delete_contact(update, _):
    global search_result
    global number_condition
    logger.my_log(update, _, f'Contact deleted: {search_result[number_condition - 1]}')
    telephone_dir = read_or_write_condition(tel_dir, 'r')
    telephone_dir.remove(search_result[number_condition - 1])
    search_result = []
    with open('telephone_directory.json', 'w') as t_d:
        json.dump(telephone_dir, t_d, indent=2, ensure_ascii=False)
    
def change_last_name(update, _):
    global search_result
    global number_condition
    if checks.check_text(update, update.message.text):
        read_or_write_change(update.message.text,'Last name')
        search_result = []
        update.message.reply_text('The contact last_name is changed.')
        return menu.start(update, _)
    else:
        return INPUT_LAST_NAME_ACTION

def change_first_name(update, _):
    global search_result
    global number_condition
    if checks.check_text(update, update.message.text):
        read_or_write_change(update.message.text, 'First name')
        search_result = []
        update.message.reply_text('The contact first_name is changed.')
        return menu.start(update, _)
    else:
        return INPUT_FIRST_NAME_ACTION

def change_telelephone(update, _):
    global search_result
    global number_condition

    if checks.check_text(update, update.message.text):
        read_or_write_change(update.message.text, 'First name')
        search_result = []
        update.message.reply_text('The contact first_name is changed.')
        return menu.start(update, _)
    else:
        return INPUT_TELEPHONE_ACTION

def change_comment(update, _):
    global search_result
    global number_condition
    if checks.check_text(update, update.message.text):
        read_or_write_change(update.message.text, 'Comment')
        search_result = []
        update.message.reply_text('The contact comment is changed.')
        return menu.start(update, _)
    else:
        return INPUT_COMMENT_ACTION
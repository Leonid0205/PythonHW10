from sqlalchemy import false


def check_text(update, text) -> bool:
    '''Function checks text length'''
    if 2 > len(text) > 10:
        update.message.reply_text('The text needs to be between 3 and 10 symbols)\n'
                              'Please try again.')
        return False
    else: 
        
        return False

def check_telephone(update, text):
    '''Function checks telphone input'''
    if len(text) != 12:
        update.message.reply_text('Telephone forman is 9991117733, twelve digits.')
        return False
    for i in text:
        if i.isalpha():
            update.message.reply_text('Telephone must contain only digits.\n'
                                      'Please try again.')
            return False
    return True

def check_choose_contact(update, text) -> bool:
    '''Function checks ID input'''
    try:
        id = int(text)
        return True
    except:
        update.message.reply_text('Incorrect input.\n'
                                  'Please try again.')
        return False
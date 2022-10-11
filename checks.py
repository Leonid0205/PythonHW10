def check_text(update, text) -> bool:
    '''Function checks text length'''
    if len(text) > 10:
        update.message.reply_text('The text needs to be more than nothing and less than 10 symbols)\n'
                              'Please try again.')
        return False
    else: 
        return True

def check_telephone(update, text) -> bool:
    '''Function checks telphone input'''
    try:
        telephone = int(text)
        if len(str(telephone)) == 10:
            return True
        else:    
            update.message.reply_text('Telephone format is 9991117733, twelve digits!!! Try again) ')
    except ValueError:
        update.message.reply_text('ValueError!\n'
                                  'Telephone format is 9991117733, twelve digits!!! Try again) ')

def check_choose_contact(update, text) -> bool:
    '''Function checks ID input'''
    try:
        id = int(text)
        return True
    except:
        update.message.reply_text('Incorrect input.\n'
                                  'Please try again.')
        return False
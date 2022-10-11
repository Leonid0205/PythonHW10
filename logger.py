from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime as dt

# def log(update: Update, context: CallbackContext):
#     time = dt.now().strftime('%H:%M')
#     with open ('log.txt', 'a') as log:
#         log.write(f'{time} - {update.effective_user.first_name},{update.effective_user.id}, {update.message.text}\n')

def my_log(update: Update, context: CallbackContext, data):
    time = dt.now().strftime('%H:%M')
    with open ('log.txt', 'a', encoding='utf-8') as log:
        log.write(f'{time} - {update.effective_user.first_name},{update.effective_user.id}, {update.message.text}\n')
        log.write(f'{time} => User - {update.effective_user.first_name} => {data}\n')
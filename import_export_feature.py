import menu
import operations_contacts
import csv
import json

tel_dir = {}

def export(update, _):
    telephone_dir = operations_contacts.read_or_write_condition(tel_dir, 'r')
    if len(telephone_dir) == 0:
        update.message.reply_text('There is no contacts to export. ')
        return menu.start(update, _)
    count = 0
    with open('telephone_directory.csv', mode = 'w', encoding = 'utf-8') as t_d_w:
        writer = csv.writer(t_d_w, delimiter = '\t', lineterminator = '\r')
        writer.writerow(['Last name', 'First name', 'Telephone', 'Comment'])
        for i in telephone_dir:
            writer.writerow([i['Last name'], i['First name'], i['Telephone'], i['Comment']])
            count += 1
    update.message.reply_text(f'Export is finished.\n')
    return menu.start(update, _)

def import_j(update, _):
    dumper = []
    with open('telephone_directory.csv', encoding = 'utf-8') as imp_read_file:
        reader = csv.reader(imp_read_file, delimiter = '\t')
        next(reader)
        try:
            for row in reader:
                    temp_dict = {}
                    temp_dict['Last name'] = row[0]
                    temp_dict['First name'] = row[1]
                    temp_dict['Telephone'] = row[2]
                    temp_dict['Comment'] = row[3]
                    dumper.append(temp_dict)
        except:
            update.message.reply_text('Sorry file is corrupted.')
            return menu.start(update, _)
    if len(dumper) == 0:
        update.message.reply_text('File for import is empty.')
        return menu.start(update, _)
    with open('telephone_directory.json', 'w') as t_d:
        json.dump(dumper, t_d, indent=2,ensure_ascii=False)
    update.message.reply_text(f'Import is finished.')
    return menu.start(update, _)
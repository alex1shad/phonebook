import re
import csv


with open('phonebook_raw.csv',  encoding='utf8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)


threeword_pattern = r'\w+\s+\w+\s+\w+'
twoword_pattern = r'\w+\s+\w+'
phone_pattern = r'(\+7|7|8)\s*(\(?\d{3}\)?)[-\s]*(\d+\-?\d+-?\d+)\s*(\(?доб\.?\s*\d+\)?)?'
email_pattern = r'(\w+?\w+?\.?\w+@minfin.ru)|(\w+\@nalog.ru)'

finish_list = []

for n, el in enumerate(contacts_list[1:]):
    finish_list.append([])
    dirty_name = el[:3]
    fio = 0
    fi = 0
    io = 0
    for i in range(len(dirty_name)):
        if i == 0:
            name = re.findall(threeword_pattern, str(dirty_name[i]))
            if len(name) > 0:
                fio = 1
                name = ''.join(name).split(' ')
                finish_list[n].append(name[0])
                finish_list[n].append(name[1])
                finish_list[n].append(name[2])
            else:
                name = re.findall(twoword_pattern, str(dirty_name[i]))
                if len(name) > 0:
                    fi = 1
                    name = ''.join(name).split(' ')
                    finish_list[n].append(name[0])
                    finish_list[n].append(name[1])
                elif fio != 1:
                    finish_list[n].append(dirty_name[i])
        if i == 1:
            name = re.findall(twoword_pattern, str(dirty_name[i]))
            if len(name) > 0:
                io = 1
                name = ''.join(name).split(' ')
                finish_list[n].append(name[0])
                finish_list[n].append(name[1])
            elif fio == 0 and fi == 0:
                finish_list[n].append(dirty_name[i])
        if i == 2:
            if fio == 0 and io == 0:
                finish_list[n].append(dirty_name[i])
    dirty_organization = el[3]
    finish_list[n].append(dirty_organization)
    dirty_position = el[4]
    finish_list[n].append(dirty_position)
    dirty_phone = re.findall(phone_pattern, el[5])
    if len(dirty_phone) != 0:
        clean_phone = ''.join(dirty_phone[0]).replace('(', '').\
            replace(')', '').\
            replace('-', '').\
            replace('+7', '8').\
            replace('8', '+7', 1).\
            replace(' ', '')
        finish_phone = f'+7({clean_phone[2:5]}){clean_phone[5:7]}-{clean_phone[7:9]}-{clean_phone[9:]}'
        if len(finish_phone) > 16:
            finish_phone = f'{finish_phone[:16]} {finish_phone[16:21]}{finish_phone[21:]}'
        finish_list[n].append(finish_phone)
    else:
        finish_list[n].append('')
    dirty_email = el[6]
    if len(dirty_email) > 0:
        finish_email = ''.join(dirty_email)
        finish_list[n].append(finish_email)
    else:
        finish_list[n].append('')

finish_list.insert(0, contacts_list[0])

for i in range(len(finish_list)):
    m = i + 1
    while m < len(finish_list):
        test = []
        for j, el in enumerate(finish_list[i]):
            if el == finish_list[m][j] or el == '' or finish_list[m][j] == '':
                test.append(1)
        if len(test) == 7:
            for k in range(len(finish_list[i])):
                if finish_list[i][k] == '':
                    finish_list[i][k] = finish_list[m][k]
                elif finish_list[m][k] == '':
                    finish_list[m][k] = finish_list[i][k]
        m += 1

i = 0
while i < len(finish_list):
    if finish_list.count(finish_list[i]) > 1:
        finish_list.remove(finish_list[i])
        i -= 1
    i += 1

with open('phonebook.csv', 'w', encoding='utf8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(finish_list)

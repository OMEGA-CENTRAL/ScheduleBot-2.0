import pathlib, time, telebot, os, filecmp, shutil, datetime
from formationData import *
from peewee import *
from threading import Thread
from telebot import types 

bot = telebot.TeleBot("")
dbUsers = SqliteDatabase(pathlib.Path('users.db'))

bot.set_my_commands([
        telebot.types.BotCommand("/start", "🔘 Включить\выключить рассылку"),
        telebot.types.BotCommand("/group", "👥 Расписание для группы"),
        telebot.types.BotCommand("/teacher", "👤 Расписание для преподавателя"),
        telebot.types.BotCommand("/full", "🏫 Общее расписание"),
        telebot.types.BotCommand("/statistics", "📈 Число пользователей"),
    ])

class User(Model):
    id = CharField()
    sheduleType = CharField()
    sheduleName = CharField()

    class Meta:
        database = dbUsers

User.create_table()

def getUser(id):
    for user in User.select():
        if(user.id == str(id)):
            data = {'id': user.id, 'sheduleType': user.sheduleType, 
                    'sheduleName': user.sheduleName}
            return data
        
    return 0 

def editUser(data):
    for user in User.select():
        if(user.id == data['id']):
            user.sheduleType = data['sheduleType']
            user.sheduleName = data['sheduleName']

            user.save()

def sendShedule(id):
        try:
        
            if(getUser(id)['sheduleType'] == 'fullShedule'):    
                with open (pathlib.Path('images', 'fullShedule.jpg'), 'rb') as file:
                    bot.send_document(id, file)

            else:
                with open (pathlib.Path('images', getUser(id)['sheduleType'], 
                                                getUser(id)['sheduleName']), 'rb') as file:
                    image = file.read()

                    bot.send_photo(id, image)
                    
        except:
            bot.send_message(id, text = 'Расписание на следуйщий день не найдено 🤔')

def telegramBot():
    @bot.message_handler(commands=['start'])
    def startMessage(message):

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text = '❌ Нет', callback_data = 'mailingRefusal')
        btn2 = types.InlineKeyboardButton(text = '✅ Да', callback_data = 'mailingAgreement')
        keyboard.add(btn1, btn2)

        if(getUser(message.from_user.id) == 0): 
            User.create(id = str(message.from_user.id), sheduleType = 'unknown', sheduleName = 'unknown', lastMessage = 'unknown')
        
        bot.send_message(message.from_user.id, text = 'Вы хотите получать расписание при его обновлении?'.format(message.from_user), reply_markup=keyboard)

    @bot.message_handler(commands=['statistics'])
    def statistics(message):
        text = 'Ботом пользуются уже {} человек! 🥳'.format(len(User.select()))
        bot.send_message(message.from_user.id, text = text.format(message.from_user))

    @bot.message_handler(commands=['group'])
    def group(message):
        keyboard = types.InlineKeyboardMarkup(row_width = 3)

        with open ('groups', 'r') as file:
            files = file.read().split()

        i = 0
        while True:
            
            if(len(files) == i + 1):
                btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i] + '.jpg')
                i += 1
                keyboard.add(btn1)
                break

            elif(len(files) == i + 2):
                btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i] + '.jpg')
                i += 1
                btn2 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i] + '.jpg')
                i += 1
                keyboard.add(btn1, btn2)
                break
            
            else:
                btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i] + '.jpg')
                i += 1
                btn2 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i] + '.jpg')
                i += 1
                btn3 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i] + '.jpg')
                i += 1
                keyboard.add(btn1, btn2, btn3)

            if(len(files) == i):
                break
        
        bot.send_message(message.from_user.id, text= "⬇️ Выберите группу ⬇️" .format(message.from_user), reply_markup=keyboard)

    @bot.message_handler(commands=['teacher'])
    def teacher(message):
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        for root, dirs, files in os.walk(pathlib.Path('images', 'teacherShedule')): 
            i = 0
            while True:
                
                if(len(files) == i + 1):
                    btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    keyboard.add(btn1)
                    break

                else:
                    btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    btn2 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    keyboard.add(btn1, btn2)
                
                if(len(files) == i):
                    break
                
        bot.send_message(message.from_user.id, text= "⬇️ Выберите преподавателя ⬇️" .format(message.from_user), reply_markup=keyboard)

    @bot.message_handler(commands=['full'])
    def full(message):
        with open (pathlib.Path('images', 'fullShedule.jpg'), 'rb') as file:
            bot.send_document(message.from_user.id, file)

    @bot.callback_query_handler(func=lambda call: True)
    def menu_inline(message):
        if(message.data == 'mailingAgreement'):

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text = 'Расписание группы', callback_data = 'studentShedule')
            btn2 = types.InlineKeyboardButton(text = 'Расписание преподавателя', callback_data = 'teacherShedule')
            btn3 = types.InlineKeyboardButton(text = 'Общее расписание', callback_data = 'fullShedule')
            keyboard.add(btn1, btn2, btn3)

            bot.send_message(message.from_user.id, text = 'Какое расписание вы хотите получать?'.format(message.from_user), reply_markup=keyboard)

        elif(message.data == 'mailingRefusal'):
            data = getUser(message.from_user.id)
            data['sheduleType'] = 'unknown'
            editUser(data) 

            bot.send_message(message.from_user.id, text= "⬇️ Используйте кнопку меню ⬇️" .format(message.from_user))

        elif(message.data == 'studentShedule'):
            data = getUser(message.from_user.id)
            data['sheduleType'] = 'studentShedule'
            editUser(data) 

            keyboard = types.InlineKeyboardMarkup(row_width = 3)

            with open ('groups', 'r') as file:
                files = file.read().split()

            i = 0
            while True:
                
                if(len(files) == i + 1):
                    btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    keyboard.add(btn1)
                    break

                elif(len(files) == i + 2):
                    btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    btn2 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    keyboard.add(btn1, btn2)
                    break
                
                else:
                    btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    btn2 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    btn3 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i])
                    i += 1
                    keyboard.add(btn1, btn2, btn3)

                if(len(files) == i):
                    break
            
            bot.send_message(message.from_user.id, text= "⬇️ Выберите группу ⬇️" .format(message.from_user), reply_markup=keyboard)

        elif(message.data == 'teacherShedule'):
            data = getUser(message.from_user.id)
            data['sheduleType'] = 'teacherShedule'
            editUser(data) 

            keyboard = types.InlineKeyboardMarkup(row_width=2)

            for root, dirs, files in os.walk(pathlib.Path('images', 'teacherShedule')): 
                i = 0
                while True:
                    
                    if(len(files) == i + 1):
                        btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i].replace('.jpg', ''))
                        i += 1
                        keyboard.add(btn1)
                        break

                    else:
                        btn1 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i].replace('.jpg', ''))
                        i += 1
                        btn2 = types.InlineKeyboardButton(text = str(files[i]).replace('.jpg', ''), callback_data = files[i].replace('.jpg', ''))
                        i += 1
                        keyboard.add(btn1, btn2)
                    
                    if(len(files) == i):
                        break
                    
            bot.send_message(message.from_user.id, text= "⬇️ Выберите преподавателя ⬇️" .format(message.from_user), reply_markup=keyboard)
                    
        elif(message.data == 'fullShedule'):
            data = getUser(message.from_user.id)
            data['sheduleType'] = 'fullShedule'
            editUser(data) 

            bot.send_message(message.from_user.id, text= "Рассылка расписания включена!" .format(message.from_user))
            sendShedule(message.from_user.id)

        elif('.jpg' in message.data):
            for root, dirs, files in os.walk(pathlib.Path('images', 'studentShedule')):
                if(message.data in files):
                    with open (pathlib.Path('images', 'studentShedule', message.data), 'rb') as file:
                        image = file.read()
                    bot.send_photo(message.from_user.id, image)

            for root, dirs, files in os.walk(pathlib.Path('images', 'teacherShedule')):
                if(message.data in files):
                    with open (pathlib.Path('images', 'teacherShedule', message.data), 'rb') as file:
                        image = file.read()
                    bot.send_photo(message.from_user.id, image)
        
        else:
            data = getUser(message.from_user.id)
            data['sheduleName'] = str(message.data) + '.jpg'
            editUser(data) 

            bot.send_message(message.from_user.id, text= "Рассылка расписания включена!" .format(message.from_user))
            sendShedule(message.from_user.id)

    bot.remove_webhook()
    bot.infinity_polling()

def scheduleDistribution():

    formationDataStudent()
    formationDataTeacher()
    formationDataAll()

    for user in User.select():
        if user.sheduleType != 'unknown':
                sendShedule(user.id)

def endlessUpdate():
    try:

        while True:

            downloadFile()
            
            if(os.path.exists('fileCopy.xlsx') == True):
                if(filecmp.cmp('file.xlsx', 'fileCopy.xlsx') == False):
                    os.remove("fileCopy.xlsx")
                    shutil.copyfile("file.xlsx", "fileCopy.xlsx")
                    scheduleDistribution()
                
            else:
                shutil.copyfile("file.xlsx", "fileCopy.xlsx")
                scheduleDistribution()

            time.sleep(10)

    except Exception as error:
        with open (pathlib.Path('errors.txt'), 'a') as file:
            file.write(str(error) + '\n')   

def startAll():
    function_1 = Thread(target = telegramBot)
    function_2 = Thread(target = endlessUpdate)

    function_1.start()
    function_2.start()

startAll()
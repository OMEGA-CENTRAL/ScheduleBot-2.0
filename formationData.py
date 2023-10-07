import pathlib, requests, time, os
import pandas as pd
from createImage import *


def downloadFile():
    try:
        url = 'https://serp-koll.ru/images/ep/k1/rasp1.xlsx'
        response = requests.get(url, timeout = 10)

        with open ('file.xlsx', 'wb') as file:
            file.write(response.content)
    except:
       ...
        
def formationDataAll():
    file = pd.read_excel('file.xlsx', header=None)
    file = file.fillna('')
    data = {'date': '', 'groups': [],}

    #дата
    data['date'] = file.iat[0,1].partition(' ')[2].partition(' ')[2]

    #группы
    for column in range(file.shape[1] - 1):
        x = 0.0
        group = file.iat[1, column + 1] 
        if(type(group) == type(x)):
            group = int(group)
        data['groups'].append(str(group))
    
    #ячейки
    for row in range(file.shape[0] - 1):
        if(file.iat[row, 0] in range(10)):
            data[file.iat[row, 0]] = {}
            for column in range(file.shape[1] - 1):
                data[file.iat[row, 0]][column + 1] = []
                data[file.iat[row, 0]][column + 1].append(file.iat[row, column + 1])
                if(file.iat[row + 1, column + 1] != ''):
                    data[file.iat[row, 0]][column + 1].append(file.iat[row + 1, column + 1])

    #создание картинки        
    createImage(data, pathlib.Path('images', 'fullShedule.jpg')) 

    with open ('groups', 'w') as file:
        for i in range(len(data['groups'])):
            if(i + 1 == len(data['groups'])):
                file.write(str(data['groups'][i]))
            else:
                file.write(str(data['groups'][i]) + ' ')
            


def formationDataStudent():
    file = pd.read_excel('file.xlsx', header=None)
    file = file.fillna('')
    data = {'date': '', 'groups': [],}

    #дата
    data['date'] = file.iat[0,1].partition(' ')[2].partition(' ')[2]

    #группы
    for column in range(file.shape[1] - 1):
        x = 0.0
        group = file.iat[1, column + 1] 
        if(type(group) == type(x)):
            group = int(group)
        data['groups'].append(str(group))
    
    #ячейки
    for row in range(file.shape[0] - 1):
        if(file.iat[row, 0] in range(10)):
            data[file.iat[row, 0]] = {}
            for column in range(file.shape[1] - 1):
                data[file.iat[row, 0]][column + 1] = []
                data[file.iat[row, 0]][column + 1].append(file.iat[row, column + 1])
                if(file.iat[row + 1, column + 1] != ''):
                    data[file.iat[row, 0]][column + 1].append(file.iat[row + 1, column + 1])
    
    #удаление прошлых файлов
    for root, dirs, files in os.walk(pathlib.Path('images', 'studentShedule')): 
        for file in files:
            os.remove(pathlib.Path('images', 'studentShedule', file))

    #создание картинок
    for a in range(len(data['groups'])):   
        group = data['groups'][a]
        dataGroup = {'date': data['date'], 'groups': [group]}
        for b in range(len(data) - 2):
            dataGroup[b + 1] = {}
            dataGroup[b + 1][1] = data[b + 1][a + 1]
        
        createImage(dataGroup, pathlib.Path('images', 'studentShedule', group + '.jpg'))   


def formationDataTeacher():
    file = pd.read_excel('file.xlsx', header=None)
    file = file.fillna('')
    data = {'date': '', 'groups': [],}
    
    #дата
    data['date'] = file.iat[0,1].partition(' ')[2].partition(' ')[2]

    #преподователи
    for row in range(file.shape[0] - 1):
        if(file.iat[row, 0] in range(10)):
            for column in range(file.shape[1] - 1):
                if(file.iat[row, column + 1] != '' and file.iat[row - 9, column + 1] != '' and file.iat[row - 9, column + 1] not in data['groups']):
                    data['groups'].append(file.iat[row - 9, column + 1])
                if(file.iat[row, column + 1] != '' and file.iat[row - 4, column + 1] != '' and file.iat[row - 4, column + 1] not in data['groups']):
                    data['groups'].append(file.iat[row - 4, column + 1])
    
    #создание row
    for row in range(file.shape[0] - 1):
        if(file.iat[row, 0] in range(10)):
            data[file.iat[row, 0]] = {}

    #формирование списков
    for a in range(len(data['groups'])):
        for b in range(len(data) - 2):
            data[b + 1][a + 1] = []

    #ячейки
    for teacher in range(len(data['groups'])):
         for row in range(file.shape[0] - 1):
            if(file.iat[row, 0] in range(10)):
                for column in range(file.shape[1] - 1):
                    
                    if(file.iat[row, column + 1] != '' and file.iat[row - 9, column + 1] != '' and file.iat[row - 9, column + 1] == data['groups'][teacher]):
                        content = (str(file.iat[1, column + 1]) + '\n' + str(file.iat[row - 11, column + 1])
                                    + '\n' + file.iat[row - 10, column + 1])
                        if(file.iat[row - 7, column + 1] != '-' and file.iat[row - 7, column + 1] != ''):
                            content += ('\n(' + file.iat[row - 7, column + 1] + ')')
                        data[file.iat[row, 0]][teacher + 1].append(content)
                        
                    if(file.iat[row, column + 1] != '' and file.iat[row - 4, column + 1] != '' and file.iat[row - 4, column + 1] == data['groups'][teacher]):
                        content = (str(file.iat[1, column + 1]) + '\n' + str(file.iat[row - 6, column + 1])
                                    + '\n' + file.iat[row - 5, column + 1])
                        if(file.iat[row - 2, column + 1] != '-' and file.iat[row - 2, column + 1] != ''):
                            content += ('\n(' + file.iat[row - 2, column + 1] + ')')
                        data[file.iat[row, 0]][teacher + 1].append(content)

    #удаление прошлых файлов
    for root, dirs, files in os.walk(pathlib.Path('images', 'teacherShedule')): 
        for file in files:
            os.remove(pathlib.Path('images', 'teacherShedule', file))

    #создание картинок
    for a in range(len(data['groups'])):   
        group = data['groups'][a]
        dataGroup = {'date': data['date'], 'groups': [group]}
        for b in range(len(data) - 2):
            dataGroup[b + 1] = {}
            dataGroup[b + 1][1] = data[b + 1][a + 1]
        
        createImage(dataGroup, pathlib.Path('images', 'teacherShedule', group + '.jpg')) 

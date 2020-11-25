import json
import jsonschema
from jsonschema import validate
import logging as log
import os

log.basicConfig(filename='README.txt',level=50, format=' %(message)s')
log.critical("\n------------start------------\n")

files=os.listdir('C:\\Users\\fujitsu\\Desktop\\Json')
Jsons=list(filter(lambda x: x.endswith('.json'), files))
Schemas=list(filter(lambda x: x.endswith('.schema'), files))
#print(Jsons)
#print(Schemas)

###проверим, всем ли приписана схема
##for Json in Jsons:
##    with open(Json) as file1:
##        try:
##            d = json.load(file1)
##            data=d.keys()
##            p=d.get('event')
##            print(Json+' eventname = '+p)
##        except:
##            print(Json+':error')
##            continue
###да, всем кроме двух пустых, и в одном ошибка


for Json in Jsons:

    JsonName=Json
    with open(JsonName) as file1:
        d = json.load(file1)
        try:
            data=d.keys()
            p=d.get('data') #dict
            if p==None:
                log.critical('\nРаздел "data" файла {} пуст\
                                \n перехожу к следующему файлу \n'.format(JsonName))
                print('Раздел "data" вашего Json пуст')
                continue

        except:
            log.critical('\n Файл {}  - на самом деле не Json. Он пуст или не соотвутствует структуре Json. \n\
                            Перехожу к следующему файлу\n'.format(JsonName))
            print('\n Файл {}  - на самом деле не Json. Перехожу к следующему файлу\n'.format(JsonName))
            continue


    for Schema in Schemas:
        SchemaName=Schema

        with open(SchemaName) as schema1:
            c = json.load(schema1) #dict


        try:
            log.critical('\n Trying to validate: \n SCHEMA = '+SchemaName+' \n JSON file= '+JsonName)
            v=jsonschema.Draft7Validator(c)
            errors=v.iter_errors(p)
            jsonschema.validate(p,c)
            log.critical("Result: SUCCESS!")

        except:
            log.critical("Result: failure!")
            log.critical("Due to:")
            for error in errors:
                log.critical(error.message)
                print(error.message)
                if error.message[-22::]=='is a required property':
                    req_prop=len(error.message)-23
                    log.critical('В файле json не хватает обязательной части: {}'.format(error.message[0:req_prop]))
                    print('В файле json не хватает обязательной части: {}'.format(error.message[0:req_prop]))



log.critical('\n Все файлы проверены')
print('Все файлы проверены')

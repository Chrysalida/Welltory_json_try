import json
import jsonschema
from jsonschema import validate
import logging as log
import os

files=os.listdir('C:\\Users\\fujitsu\\Desktop\\Json')
Jsons=list(filter(lambda x: x.endswith('.json'), files))
Schemas=list(filter(lambda x: x.endswith('.schema'), files))

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
###но проверять все равно будем все



def validating(Jsons,Schemas):
    """
    reports errors in Json files

    takes 2 lists: list of jsons and list of schemas
    checks each json against each schema
    prints human-readable commentary on each error into the Readme.txt
    otherwise declares success
    reports when all files are checked
    requires jsonschema lib

    """



    log.basicConfig(filename='README.txt',level=50, format=' %(message)s')
    log.critical("\n------------start------------\n")

    for Json in Jsons:

        JsonName=Json
        with open(JsonName) as file1:
            d = json.load(file1)
            try:
                data=d.keys()
                p=d.get('data') #dict
                if p==None:
                    log.critical('\nРаздел "data" файла {} пуст,\
                                    \nэто значит, что смысловая часть данных отсуствует.\
                                    \nПерехожу к следующему файлу \n'.format(JsonName))
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
                    err_mess=error.message
                    error_interpret(err_mess)


    log.critical('\n Все файлы проверены')
    print('Все файлы проверены')




def error_interpret(error_message):
    """
    Makes human-readable report on each validation error

    takes error.message as an input
    check error.message against different error criteria
    (e.g. required property absent, data of the wrong type etc)
    error.message comes from iter_errors (jsonschema.Draft7Validator lib)

    """

    notoftype=' is not of type '
    a=error_message.find(notoftype,0)
    if not a==-1:#if this error is not-of-type error:
        prop=error_message[0:a]#what property is of the wrong type?
        tp=len(notoftype)+a#where in the error message the type is determined?
        data_type=error_message[tp::]#and finally, what the type it should be?
        log.critical('Неправильный тип данных у {0}. Замените на данные типа {1}'.format(prop,data_type))
        print('Неправильный тип данных у {0}. Требуемый тип данных: {1}'.format(prop,data_type))

    elif error_message[-22::]=='is a required property':
        req_prop=len(error_message)-23
        log.critical('В файле json не хватает обязательной части: {}, добавьте ее.'.format(error_message[0:req_prop]))
        print('В файле json не хватает обязательной части: {}'.format(error_message[0:req_prop]))
    else:
        log.critical(error_message)
        print(error_message)



validating(Jsons,Schemas)

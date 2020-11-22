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

#проверим, всем ли приписана схема
for Json in Jsons:
    with open(Json) as file1:
        try:
            d = json.load(file1)
            data=d.keys()
            p=d.get('event')
            print(Json+' eventname = '+p)
        except:
            print(Json+':error')
            continue
#да, всем кроме двух пустых, и в одном ошибка

JsonName='a95d845c-8d9e-4e07-8948-275167643a40.json'
with open(JsonName) as file1:
    d = json.load(file1)
    data=d.keys()
    p=d.get('data') #dict


for Schema in Schemas:
    SchemaName=Schema

    with open(SchemaName) as schema1:
        c = json.load(schema1) #dict


    try:
        log.critical('\n Trying to validate: \n SCHEMA = '+SchemaName+' \n JSON file= '+JsonName)
        v=jsonschema.Draft7Validator(c)
        errors=v.iter_errors(p)
        jsonschema.validate(p,c)
        log.critical("Result: success")

    except:
        log.critical("Result: failure!")
        log.critical("Due to:")
        for error in errors:
            log.critical(error.message)
            print(error.message)
            if error.message=="None is not of type 'object'":
                log.critical('Возможно, ваш Json пуст')
                print('Возможно, ваш Json пуст')

import json
import jsonschema
from jsonschema import validate
import logging as log

log.basicConfig(filename='README.txt',level=50, format=' %(message)s')
log.critical("\n------------start------------\n")


JsonName='1eba2aa1-2acf-460d-91e6-55a8c3e3b7a3.json'
with open(JsonName) as file1:
    d = json.load(file1)
    data=d.keys()
    p=d.get('data')

    print(type(p))


SchemaName='label_selected.schema'
with open(SchemaName) as schema1:
    c = json.load(schema1)

    print(type(c))


try:
    log.critical('Trying to validate: \n SCHEMA = '+SchemaName+' \n JSON file= '+JsonName)
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





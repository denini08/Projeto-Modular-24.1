import json
from typing import List

def read_db(pathToFile: str) -> List:
    try:
        with open(pathToFile, mode="r") as jsonFile:
            database = json.load(jsonFile)
        return database["data"] # Sucesso
    except (FileNotFoundError, PermissionError):
        return -4 # Nao achou o banco
    except Exception as ex:
        print(ex)
        return [] # Nao achou o banco

def write_db(obj_list: List[object], primaryKey, pathToFile: str) -> int:
    try:
        with open(pathToFile, mode="r") as jsonFile:
            data = json.load(jsonFile)
            newData = data
    except (FileNotFoundError, PermissionError):
        return -4 # Nao achou db
    try:
        if len(data["data"]) > 0:
            first_obj_keys = set(data["data"][0].keys())
        else:
            first_obj_keys = None

        for obj in obj_list:
            new_obj_keys = set(obj.keys())

            if first_obj_keys != new_obj_keys and first_obj_keys != None:
                return -3  # Objeto a ser inserido tem chaves diferentes dos do banco

            if any(item[primaryKey] == obj[primaryKey] for item in newData["data"]):
                return -1 # Essa chave primaria ja existe

            newData["data"].append(obj)

        with open(pathToFile, mode="w") as jsonFile:
            json.dump(newData, jsonFile)

        return 1 # Sucesso

    except Exception as ex:
        print(ex)
        with open(pathToFile, mode="w") as jsonFile:
            json.dump(data, jsonFile)
        return -2 # Erro nao mapeado, nao salva nada
 
def update_db(obj: object, primaryKey: str, pathToFile: str) -> int:
    try:
        with open(pathToFile, mode="r") as jsonFile:
            data = json.load(jsonFile)
    except (FileNotFoundError, PermissionError):
        return -4 # Nao achou db
    try:
        if len(data["data"]) > 0:
            first_obj_keys = set(data["data"][0].keys())
            new_obj_keys = set(obj.keys())
            if first_obj_keys != new_obj_keys:
                return -3  # Objeto a ser inserido tem chaves diferentes dos do banco

        index = next((i for i, item in enumerate(data["data"]) if item[primaryKey] == obj[primaryKey]), None)

        if index is not None:
            data["data"][index] = obj
        else:
            return -1 # Nao achou o objeto

        with open(pathToFile, mode="w") as jsonFile:
            json.dump(data, jsonFile)

        return 1 # Sucesso

    except Exception as ex:
        print(ex)
        return -2 # Erro nao mapeado
    
def delete_db(object:object, primaryKey:str,  pathToFile: str) -> int:
    try:
        with open(pathToFile, mode="r") as jsonFile:
            data = json.load(jsonFile)
    except (FileNotFoundError, PermissionError):
        return -4 # Nao achou db
    try:
        index = next((i for i, item in enumerate(data["data"]) if item[primaryKey] == object[primaryKey]), None)

        if index is not None:
            del data["data"][index]
        else:
            return -1

        with open(pathToFile, mode="w") as jsonFile:
            json.dump(data, jsonFile)

        return 1

    except Exception as ex:
        print(ex)
        return -2



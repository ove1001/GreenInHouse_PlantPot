import traceback
from datetime import datetime
from http import HTTPStatus
from flask import current_app
from typing import List, Dict
from backend.service import RegistroSensorService, SensorService, PlantaService
from common.data.util import RegistroSensor as RegistroSensorCommon, Sensor as SensorCommon, Planta as PlantaCommon
from common.data.util import TipoSensor, ZonaSensor, TipoMedida, UnidadMedida

def get(rsid: int) -> Dict:
    with current_app.app_context() :
        if RegistroSensorService.exists(current_app.db,rsid):
            return RegistroSensorService.get(current_app.db, rsid).toJson(), HTTPStatus.OK.value
        else:
            return ("El registro de sensor " + str(rsid) + "no existe", HTTPStatus.NOT_FOUND.value)
        
def getAll() -> List[Dict]:
    with current_app.app_context() :
        return [item.toJson() for item in RegistroSensorService.listAll(current_app.db)], HTTPStatus.OK.value

def getAllFromSensor(st:str, sz: str ,sid:int) -> List[Dict]:
    try:
        tipo_sensor:TipoSensor = TipoSensor[st]
    except(KeyError):
        return ("El tipo de sensor " + str(st) + " no existe.", HTTPStatus.NOT_ACCEPTABLE.value)   
    try:
        zona_sensor: ZonaSensor = ZonaSensor[sz]
    except(KeyError):
        return ("La zona de sensor " + str(sz) + " no existe.", HTTPStatus.NOT_ACCEPTABLE.value)   
    numero_sensor:int = sid
    with current_app.app_context() :
        if SensorService.exists(current_app.db,tipo_sensor,zona_sensor,numero_sensor):
            return [item.toJson() for item in RegistroSensorService.listAllFromSensor(current_app.db,tipo_sensor,zona_sensor,numero_sensor)], HTTPStatus.OK.value
        else:
            return ("El sensor " + str(numero_sensor) + " de tipo " + str(tipo_sensor) + " de la zona " + str(zona_sensor) + " no existe", HTTPStatus.NOT_FOUND.value)

def getAllFromSensorBetweenDates(st:str, sz: str ,sid:int, fi: str, ff: str = str(datetime.now())) -> List[Dict]:
    try:
        tipo_sensor:TipoSensor = TipoSensor[st]
    except(KeyError):
        return ("El tipo de sensor " + str(st) + " no existe.", HTTPStatus.NOT_ACCEPTABLE.value)   
    try:
        zona_sensor: ZonaSensor = ZonaSensor[sz]
    except(KeyError):
        return ("La zona de sensor " + str(sz) + " no existe.", HTTPStatus.NOT_ACCEPTABLE.value)   
    numero_sensor:int = sid
    try:
        fecha_inicio=datetime.fromisoformat(fi)
    except(ValueError):
        return ("Error en el formato de la fecha de inicio " + str(fi) +" .", HTTPStatus.NOT_ACCEPTABLE.value)
    try:
        fecha_fin=datetime.fromisoformat(ff)
    except(ValueError):
        return ("Error en el formato de la fecha de fin " + str(ff) +" .", HTTPStatus.NOT_ACCEPTABLE.value)
    if fecha_inicio > fecha_fin:
        return ("La fecha de inicio " + str(fi) + " no puede ser mayor que la fecha de fin " + str(ff) + " .", HTTPStatus.NOT_ACCEPTABLE.value)
    with current_app.app_context() :
        if SensorService.exists(current_app.db,tipo_sensor,zona_sensor,numero_sensor):
            return [item.toJson() for item in RegistroSensorService.listAllFromSensorBetweenDates(current_app.db,tipo_sensor,zona_sensor,numero_sensor,
                                                                                                    fecha_inicio,fecha_fin)], HTTPStatus.OK.value
        else:
            return ("El sensor " + str(numero_sensor) + " de tipo " + str(tipo_sensor) + " de la zona " + str(zona_sensor) + " no existe", HTTPStatus.NOT_FOUND.value)

def getAllFromPlant(np:str) -> List[Dict]:
    with current_app.app_context() :
        if PlantaService.exists(current_app.db,np):
            nombre_planta: str = np
            return [item.toJson() for item in RegistroSensorService.listAllFromPlant(current_app.db, nombre_planta)], HTTPStatus.OK.value
        else:
            return ("La planta " + np + " no existe.", HTTPStatus.NOT_FOUND.value)

def getAllFromPlantBetweenDates(np:str, fi: str, ff: str = str(datetime.now())) -> List[Dict]:
    try:
        fecha_inicio=datetime.fromisoformat(fi)
    except(ValueError):
        return ("Error en el formato de la fecha de inicio " + str(fi) +" .", HTTPStatus.NOT_ACCEPTABLE.value)
    try:
        fecha_fin=datetime.fromisoformat(ff)
    except(ValueError):
        return ("Error en el formato de la fecha de fin " + str(ff) +" .", HTTPStatus.NOT_ACCEPTABLE.value)
    if fecha_inicio > fecha_fin:
        return ("La fecha de inicio " + str(fi) + " no puede ser mayor que la fecha de fin " + str(ff) + " .", HTTPStatus.NOT_ACCEPTABLE.value)
    with current_app.app_context() :
        if PlantaService.exists(current_app.db,np):
            nombre_planta: str = np
            return [item.toJson() for item in RegistroSensorService.listAllFromPlantBetweenDates(current_app.db, nombre_planta, fecha_inicio, fecha_fin)], HTTPStatus.OK.value
        else:
            return ("La planta " + np + " no existe.", HTTPStatus.NOT_FOUND.value)   

def __fromListToGraph(lista_registros: List[Dict]):
    dic_registros_clasificados: Dict = RegistroSensorService.processListForGraph(lista_registros)
    dic_registros_graficar = {}
    dic_registros_graficar["TEMPERATURA"] = {}
    dic_registros_graficar["TEMPERATURA"]["AMBIENTE"] = dic_registros_clasificados.get("TEMPERATURA").get("AMBIENTE")
    dic_registros_graficar["HUMEDAD"] = {}
    dic_registros_graficar["HUMEDAD"]["AMBIENTE"] = dic_registros_clasificados.get("HUMEDAD").get("AMBIENTE")
    dic_registros_graficar["HUMEDAD"]["MACETA"] = dic_registros_clasificados.get("HUMEDAD").get("MACETA")
    return dic_registros_graficar

def getAllFromPlantToGraph(np:str) -> List[Dict]:
    with current_app.app_context() :
        if PlantaService.exists(current_app.db,np):
            nombre_planta: str = np
            lista_registros = RegistroSensorService.listAllFromPlant(current_app.db, nombre_planta)
            try:
                dic_registros_graficar = __fromListToGraph(lista_registros)
            except:
                return ("Error al procesar los datos de la planta " + np + " para graficar.", HTTPStatus.NOT_FOUND.value)
            return dic_registros_graficar, HTTPStatus.OK.value
        else:
            return ("La planta " + np + " no existe.", HTTPStatus.NOT_FOUND.value)

def getAllFromPlantBetweenDatesToGraph(np:str, fi: str, ff: str = str(datetime.now())) -> List[Dict]:
    try:
        fecha_inicio=datetime.fromisoformat(fi)
    except(ValueError):
        return ("Error en el formato de la fecha de inicio " + str(fi) +" .", HTTPStatus.NOT_ACCEPTABLE.value)
    try:
        fecha_fin=datetime.fromisoformat(ff)
    except(ValueError):
        return ("Error en el formato de la fecha de fin " + str(ff) +" .", HTTPStatus.NOT_ACCEPTABLE.value)
    if fecha_inicio > fecha_fin:
        return ("La fecha de inicio " + str(fi) + " no puede ser mayor que la fecha de fin " + str(ff) + " .", HTTPStatus.NOT_ACCEPTABLE.value)
    with current_app.app_context() :
        if PlantaService.exists(current_app.db,np):
            nombre_planta: str = np
            lista_registros = RegistroSensorService.listAllFromPlantBetweenDates(current_app.db, nombre_planta, fecha_inicio, fecha_fin)
            try:
                dic_registros_graficar = __fromListToGraph(lista_registros)
            except:
                return ("Error al procesar los datos de la planta " + np + " para graficar.", HTTPStatus.NOT_FOUND.value)
            return dic_registros_graficar, HTTPStatus.OK.value
        else:
            return ("La planta " + np + " no existe.", HTTPStatus.NOT_FOUND.value) 
        

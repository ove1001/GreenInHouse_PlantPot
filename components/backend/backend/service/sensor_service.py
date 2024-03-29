#Author: Oscar Valverde Escobar

from datetime import datetime
from typing import Union, List, Dict
from sqlalchemy.orm.session import Session # type: ignore
import backend.service as service
from backend.data.db.esquema import Esquema
from backend.data.db.results import Sensor
from backend.data.db.resultsets import SensorSet
from backend.service.sensor_planta_service import SensorPlantaService
from common.data.util import Sensor as SensorCommon, SensorPlanta as SensorPlantaCommon
from common.data.util import TipoSensor, ZonaSensor, ModeloSensor, TipoMedida, UnidadMedida

class SensorService():
    
    @staticmethod
    def create(esquema: Esquema, tipo_sensor:TipoSensor, zona_sensor: ZonaSensor ,numero_sensor:int, modelo_sensor:ModeloSensor, nombre_sensor: str,
                               direccion_lectura:str=None, patilla_0_lectura:int=None, patilla_1_lectura:int=None, 
                               patilla_2_lectura:int=None, patilla_3_lectura:int=None, unidad_medida_0:UnidadMedida = UnidadMedida.SIN_UNIDAD,
                               unidad_medida_1:UnidadMedida = UnidadMedida.SIN_UNIDAD, unidad_medida_2:UnidadMedida = UnidadMedida.SIN_UNIDAD,
                               unidad_medida_3:UnidadMedida = UnidadMedida.SIN_UNIDAD, fecha_creacion: datetime = datetime.now() ,
                               fecha_eliminacion: datetime = None, asociar_plantas_activas=True) -> SensorCommon:
        session: Session = esquema.new_session()
        out: SensorCommon = None
        try:
            nuevo_sensor: Sensor = SensorSet.create(session, tipo_sensor, zona_sensor, numero_sensor, modelo_sensor, nombre_sensor,
                                                  direccion_lectura, patilla_0_lectura, patilla_1_lectura, 
                                                  patilla_2_lectura, patilla_3_lectura, unidad_medida_0, unidad_medida_1, 
                                                  unidad_medida_2, unidad_medida_3, fecha_creacion, fecha_eliminacion)
            out= SensorCommon(nuevo_sensor.tipo_sensor, nuevo_sensor.zona_sensor, nuevo_sensor.numero_sensor, 
                              nuevo_sensor.modelo_sensor, nuevo_sensor.nombre_sensor,
                              nuevo_sensor.direccion_lectura, nuevo_sensor.patilla_0_lectura, nuevo_sensor.patilla_1_lectura,
                              nuevo_sensor.patilla_2_lectura, nuevo_sensor.patilla_3_lectura, nuevo_sensor.unidad_medida_0,
                              nuevo_sensor.unidad_medida_1, nuevo_sensor.unidad_medida_2, nuevo_sensor.unidad_medida_3,
                              nuevo_sensor.fecha_creacion, nuevo_sensor.fecha_eliminacion)
            if asociar_plantas_activas:
                for planta in service.planta_service.PlantaService.listAllActive(esquema):
                    SensorPlantaService.createRelationFromCommon(esquema, out, planta)
        except Exception as ex:
            raise ex
        finally:
            esquema.remove_session()
        return out
    
    @staticmethod
    def createFromCommon(esquema: Esquema, sensor: SensorCommon) -> SensorCommon:
        return SensorService.create(esquema=esquema, tipo_sensor=sensor.getTipoSensor(), zona_sensor=sensor.getZonaSensor(), numero_sensor=sensor.getNumeroSensor(), 
                                    modelo_sensor=sensor.getModeloSensor(), nombre_sensor=sensor.getNombreSensor(), 
                                    direccion_lectura=sensor.getDireccionLectura(), patilla_0_lectura=sensor.getPatillaLectura(0), 
                                    patilla_1_lectura=sensor.getPatillaLectura(1), patilla_2_lectura=sensor.getPatillaLectura(2), 
                                    patilla_3_lectura=sensor.getPatillaLectura(3), unidad_medida_0=sensor.getUnidadMedida(0),
                                    unidad_medida_1=sensor.getUnidadMedida(1), unidad_medida_2=sensor.getUnidadMedida(2), 
                                    unidad_medida_3=sensor.getUnidadMedida(3)
                                    #,sensor.getFechaCreacion(), sensor.getFechaEliminacion()
                                    )

    @staticmethod
    def exists(esquema: Esquema, tipo_sensor:TipoSensor, zona_sensor: ZonaSensor ,numero_sensor:int) -> bool:
        session: Session = esquema.new_session()
        sensor_existe: bool = SensorSet.get(session, tipo_sensor, zona_sensor, numero_sensor)
        esquema.remove_session()
        return sensor_existe

    @staticmethod
    def listToJson(sensores: List[SensorCommon]) -> List[Dict]:
        out: List[Dict] = []
        for sensor in sensores:
            out.append(sensor.toJson())
        return out
    
    @staticmethod
    def listAll(esquema: Esquema) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAll(session)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor,sensor.zona_sensor,sensor.numero_sensor,
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out

    @staticmethod
    def listAllActive(esquema: Esquema) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllActive(session)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor,
                                    sensor.modelo_sensor, sensor.nombre_sensor, 
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out
    
    @staticmethod
    def listAllFromType(esquema: Esquema, tipo_sensor: TipoSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllFromType(session,tipo_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor,
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out

    @staticmethod
    def listAllActiveFromType(esquema: Esquema, tipo_sensor: TipoSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllActiveFromType(session,tipo_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor,
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out
    
    @staticmethod
    def listAllFromZone(esquema: Esquema, zona_sensor: ZonaSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllFromZone(session,zona_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor, 
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out

    @staticmethod
    def listAllActiveFromZone(esquema: Esquema, zona_sensor: ZonaSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllActiveFromZone(session,zona_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor, 
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out
    
    @staticmethod
    def listAllFromTypeAndZone(esquema: Esquema, tipo_sensor: TipoSensor, zona_sensor: ZonaSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllFromTypeAndZone(session,tipo_sensor,zona_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor, 
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out

    @staticmethod
    def listAllActiveFromTypeAndZone(esquema: Esquema, tipo_sensor: TipoSensor, zona_sensor: ZonaSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllActiveFromTypeAndZone(session,tipo_sensor,zona_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor,
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out

    @staticmethod
    def listAllFromModel(esquema: Esquema, modelo_sensor: ModeloSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllFromModel(session,modelo_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor,
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out

    @staticmethod
    def listAllActiveFromModel(esquema: Esquema, modelo_sensor: ModeloSensor) -> List[SensorCommon]:
        out: List[SensorCommon] = []
        session: Session = esquema.new_session()
        registros_sensor: List[Sensor] = SensorSet.listAllActiveFromModel(session,modelo_sensor)
        for sensor in registros_sensor:
            out.append(SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor,
                                    sensor.modelo_sensor, sensor.nombre_sensor,
                                    sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                                    sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                                    sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                                    sensor.fecha_creacion, sensor.fecha_eliminacion))
        esquema.remove_session()
        return out

    @staticmethod
    def get(esquema: Esquema, tipo_sensor:TipoSensor, zona_sensor: ZonaSensor ,numero_sensor:int) -> SensorCommon:
        session : Session = esquema.new_session()
        sensor : Sensor = SensorSet.get(session, tipo_sensor, zona_sensor, numero_sensor)
        out= SensorCommon(sensor.tipo_sensor, sensor.zona_sensor, sensor.numero_sensor,
                            sensor.modelo_sensor, sensor.nombre_sensor,
                            sensor.direccion_lectura, sensor.patilla_0_lectura, sensor.patilla_1_lectura,
                            sensor.patilla_2_lectura, sensor.patilla_3_lectura, sensor.unidad_medida_0,
                            sensor.unidad_medida_1, sensor.unidad_medida_2, sensor.unidad_medida_3,
                            sensor.fecha_creacion, sensor.fecha_eliminacion)
        esquema.remove_session()
        return out
    
    @staticmethod
    def getSensorFromRelationFromCommon(esquema: Esquema, sensor_planta : SensorPlantaCommon) -> SensorCommon:
        return SensorService.get(esquema, sensor_planta.getTipoSensor(), sensor_planta.getZonaSensor(), sensor_planta.getNumeroSensor())


    @staticmethod
    def update(esquema: Esquema, tipo_sensor:TipoSensor, zona_sensor: ZonaSensor ,numero_sensor:int, 
                modelo_sensor:ModeloSensor, nombre_sensor: str, direccion_lectura:str, patilla_0_lectura:int, patilla_1_lectura:int, 
                patilla_2_lectura:int, patilla_3_lectura:int, unidad_medida_0:UnidadMedida, unidad_medida_1:UnidadMedida,
                unidad_medida_2:UnidadMedida, unidad_medida_3:UnidadMedida, fecha_creacion: datetime,
                fecha_eliminacion: datetime) -> SensorCommon:
        session: Session = esquema.new_session()
        out: SensorCommon = None
        try:
            sensor_modificado: Sensor = SensorSet.update(session, tipo_sensor, zona_sensor, numero_sensor, 
                                                         modelo_sensor, nombre_sensor, 
                                                        direccion_lectura, patilla_0_lectura, patilla_1_lectura, 
                                                        patilla_2_lectura, patilla_3_lectura, unidad_medida_0, 
                                                        unidad_medida_1, unidad_medida_2, unidad_medida_3,
                                                        fecha_creacion, fecha_eliminacion)
            out= SensorCommon(sensor_modificado.tipo_sensor,sensor_modificado.zona_sensor,sensor_modificado.numero_sensor,
                              sensor_modificado.modelo_sensor, sensor_modificado.nombre_sensor, 
                              sensor_modificado.direccion_lectura, sensor_modificado.patilla_0_lectura, 
                              sensor_modificado.patilla_1_lectura, sensor_modificado.patilla_2_lectura, sensor_modificado.patilla_3_lectura, 
                              sensor_modificado.unidad_medida_0, sensor_modificado.unidad_medida_1, sensor_modificado.unidad_medida_2, 
                              sensor_modificado.unidad_medida_3, sensor_modificado.fecha_creacion, sensor_modificado.fecha_eliminacion)
        except Exception as ex:
            raise ex
        finally:
            esquema.remove_session()
        return out
    
    @staticmethod
    def updateFromCommon(esquema: Esquema, sensor: SensorCommon) -> SensorCommon:
        return SensorService.update(esquema, sensor.getTipoSensor(), sensor.getZonaSensor(),sensor.getNumeroSensor(), 
                                    sensor.getModeloSensor(), sensor.getNombreSensor(), 
                                    sensor.getDireccionLectura(), sensor.getPatillaLectura(0), 
                                    sensor.getPatillaLectura(1), sensor.getPatillaLectura(2), sensor.getPatillaLectura(3),
                                    sensor.getUnidadMedida(0), sensor.getUnidadMedida(1), sensor.getUnidadMedida(2), 
                                    sensor.getUnidadMedida(3), sensor.getFechaCreacion(), sensor.getFechaEliminacion())

    @staticmethod
    def unsubscribe(esquema: Esquema, tipo_sensor:TipoSensor, zona_sensor: ZonaSensor ,numero_sensor:int) -> SensorCommon:
        sensor: SensorCommon = SensorService.get(esquema, tipo_sensor, zona_sensor, numero_sensor)
        if sensor.getFechaEliminacion() is None:
            sensor.setFechaEliminacion(datetime.now())
            sensor = SensorService.updateFromCommon(esquema, sensor)
        SensorPlantaService.unsubscribeAllFromSensorFromCommon(esquema, sensor)
        return sensor

    @staticmethod
    def unsubscribeFromCommon(esquema: Esquema, sensor: SensorCommon) -> SensorCommon:
        return SensorService.unsubscribe(esquema, sensor.getTipoSensor(),sensor.getZonaSensor(),sensor.getNumeroSensor())


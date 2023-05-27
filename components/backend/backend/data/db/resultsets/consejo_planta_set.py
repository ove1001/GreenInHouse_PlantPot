from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from backend.data.db.results import Planta, ConsejoPlanta
from common.data.util import ZonaSensor, TipoMedida, UnidadMedida
from backend.data.db.exc import ErrorConsejoPlantaExiste, ErrorConsejoPlantaNoExiste

class ConsejoPlantaSet():
    """ 
    Clase responsable a nivel de tabla de las operaciones con los registros.
    """
    @staticmethod
    def create(session: Session, descripcion: str, nombre_planta:str, zona_consejo:ZonaSensor,
                 tipo_medida:TipoMedida, unidad_medida:UnidadMedida, valor_minimo:float, 
                 valor_maximo:float, horas_minimas:float, horas_maximas:float) -> ConsejoPlanta:
        """
        Creacion de un nuevo consejo de una planta.

        Nota:
            Realiza commit de la transaccion.

        Args:
            - session (Session): Objeto de sesion.
            - descripcion (str): Descripcion de los consejos de la planta
            - nombre_planta (str): Nombre de planta.
            - zona_consejo (ZonaSensor): Zona asociada al consejo
            - tipo_medida (TipoMedida): Tipo medida asociada al consejo
            - unidad_medida (UnidadMedida): 
            - valor_minimo: (float): 
            - valor_maximo (float): 
            - horas_minimas (float): 
            - horas_maximas (float): 

        Raises:
            - ValueError: Si no es proporcionado alguno de los datos necesarios.
            - ErrorConsejoPlantaExiste: Si el consejo del la planta de esa zona y tipo de medida especificados ya existe

        Returns:
            - Sensor: Registro creado del sensor.
        """
        if descripcion is None:
            raise ValueError('Necesario especificar la descripcion de los consejos de la planta.')
        if nombre_planta is None:
            raise ValueError('Necesario especificar la planta a la que se aplicaran los consejos.')
        if zona_consejo is None:
            raise ValueError('Necesario especificar la zona en la que se aplicaran los consejos de la planta.')
        if tipo_medida is None:
            raise ValueError('Necesario especificar el tipo de medida de los consejos de la planta.')
        if unidad_medida is None:
            raise ValueError('Necesario especificar la unidad de medida de los consejos de la planta.')
        if valor_minimo is None:
            raise ValueError('Necesario especificar el valor minimo del consejo de la planta.')
        if valor_maximo is None:
            raise ValueError('Necesario especificar el valor maximo del consejo de la planta.')

        nuevo_consejo = None
        try:
            nuevo_consejo = ConsejoPlanta(descripcion, nombre_planta, zona_consejo,
                                            tipo_medida, unidad_medida, valor_minimo,
                                            valor_maximo, horas_minimas, horas_maximas)
            session.add(nuevo_consejo)
            session.commit()
        except IntegrityError as ex:
            session.rollback()
            raise ErrorConsejoPlantaExiste(
                'El consejo de la planta ' + str(nombre_planta) + ' para la medida ' + str(tipo_medida) +
                ' en la zona ' + str(zona_consejo) + ' ya está registrado.'
                ) from ex
        finally:
            return nuevo_consejo

    @staticmethod
    def listAll(session: Session) -> List[ConsejoPlanta]:
        """
        Listado de consejos de una planta.

        Args:
            - session (Session): Objeto de sesion.

        Returns:
            - List[ConsejoPlanta]: Listado de consejos de una planta.
        """
        query = session.query(ConsejoPlanta)
        return query.all()

    @staticmethod
    def listAllFromPlant(session: Session, nombre_planta: str) -> List[ConsejoPlanta]:
        """
        Listado de consejos de una planta especifica.

        Args:
            - session (Session): Objeto de sesion.
            - nombre_planta (str): Nombre de planta.

        Returns:
            - List[ConsejoPlanta]: Listado de consejos de una planta.
        """
        consejos = None
        query = session.query(ConsejoPlanta).filter_by(nombre_elemento=nombre_planta)
        consejos: List[ConsejoPlanta] = query.all()
        return consejos
    
    @staticmethod
    def listAllFromZone(session: Session, zona_consejo: ZonaSensor) -> List[ConsejoPlanta]:
        """
        Listado de consejos de una zona especifica.

        Args:
            - session (Session): Objeto de sesion.
            - zona_consejo (ZonaSensor): Zona asociada al consejo.

        Returns:
            - List[ConsejoPlanta]: Listado de consejos de una planta.
        """
        consejos = None
        query = session.query(ConsejoPlanta).filter_by(zona_consejo=zona_consejo)
        consejos: List[ConsejoPlanta] = query.all()
        return consejos
    
    @staticmethod
    def listAllFromTypeMeasure(session: Session, tipo_medida: TipoMedida) -> List[ConsejoPlanta]:
        """
        Listado de consejos de un tipo de media especifico.

        Args:
            - session (Session): Objeto de sesion.
            - tipo_medida (TipoMedida): Tipo de medida.

        Returns:
            - List[ConsejoPlanta]: Listado de consejos de una planta.
        """
        consejos = None
        query = session.query(ConsejoPlanta).filter_by(tipo_medida=tipo_medida)
        consejos: List[ConsejoPlanta] = query.all()
        return consejos
    
    @staticmethod
    def listAllFromPlantAndZone(session: Session, nombre_planta: str, zona_consejo: ZonaSensor) -> List[ConsejoPlanta]:
        """
        Listado de consejos de una planta y zona especificos.

        Args:
            - session (Session): Objeto de sesion.
            - nombre_planta (str): Nombre de planta.
            - zona_consejo (ZonaSensor): Zona asociada al consejo.

        Returns:
            - List[ConsejoPlanta]: Listado de consejos de una planta.
        """
        consejos = None
        query = session.query(ConsejoPlanta).filter_by(nombre_elemento=nombre_planta, zona_consejo=zona_consejo)
        consejos: List[ConsejoPlanta] = query.all()
        return consejos
    
    @staticmethod
    def listAllFromPlantAndTypeMeasure(session: Session, nombre_planta: str, tipo_medida: TipoMedida) -> List[ConsejoPlanta]:
        """
        Listado de consejos de una planta y tipo de medida especifico.

        Args:
            - session (Session): Objeto de sesion.
            - nombre_planta (str): Nombre de planta.
            - tipo_medida (TipoMedida): Tipo de medida.

        Returns:
            - List[ConsejoPlanta]: Listado de consejos de una planta.
        """
        consejos = None
        query = session.query(ConsejoPlanta).filter_by(nombre_elemento=nombre_planta, tipo_medida=tipo_medida)
        consejos: List[ConsejoPlanta] = query.all()
        return consejos
    
    @staticmethod
    def get(session: Session, nombre_planta: str, zona_consejo:ZonaSensor, tipo_medida:TipoMedida) -> Optional[ConsejoPlanta]:
        """ 
        Obtencvion de consejo de una planta, zona y tipo de medida especificos.

        Args:
            - session (Session): Objeto de sesion.
            - nombre_planta (str): Nombre de planta.
            - zona_consejo (ZonaSensor): Zona asociada al consejo.
            - tipo_medida (TipoMedida): Tipo de medida.

        Raises:
            - ValueError: Si no es proporcionado alguno de los datos necesarios.
            - ErrorConsejoPlantaNoExiste: Si el consejo del tipo
                    de planta de esa zona y tipo de medida especificados no existe

        Returns:
            - Optional[ConsejoPlanta]: The question 
        """
        if nombre_planta is None:
            raise ValueError('Necesario especificar la planta a la que se aplicaran los consejos.')
        if zona_consejo is None:
            raise ValueError('Necesario especificar la zona en la que se aplicaran los consejos de la planta.')
        if tipo_medida is None:
            raise ValueError('Necesario especificar el tipo de medida de los consejos de la planta.')
        consejo: ConsejoPlanta = None
        try:
            query = session.query(ConsejoPlanta).filter_by(nombre_elemento=nombre_planta, zona_consejo=zona_consejo, tipo_medida=tipo_medida)
            consejo: ConsejoPlanta = query.one()
        except NoResultFound as ex:
            raise ErrorConsejoPlantaNoExiste(
                'El consejo de la planta ' + str(nombre_planta) + ' para la medida ' + str(tipo_medida) +
                ' en la zona ' + str(zona_consejo) + ' ya está registrado.'
                ) from ex
        finally:
            return consejo

    @staticmethod
    def update(session: Session, descripcion: str, nombre_planta:str, zona_consejo:ZonaSensor,
                tipo_medida:TipoMedida, unidad_medida:UnidadMedida, valor_minimo:float, 
                valor_maximo:float, horas_minimas:float, horas_maximas:float) -> ConsejoPlanta:
        """
        Modificacion de un consejo de una planta.

        Nota:
            Realiza commit de la transaccion.

        Args:
            - session (Session): Objeto de sesion.
            - descripcion (str): Descripcion de los consejos de la planta
            - nombre_planta (str): Nombre de planta.
            - zona_consejo (ZonaSensor): Zona asociada al consejo
            - tipo_medida (TipoMedida): Tipo medida asociada al consejo
            - unidad_medida (UnidadMedida): 
            - valor_minimo: (float): 
            - valor_maximo (float): 
            - horas_minimas (float): 
            - horas_maximas (float):        

        Raises:
            - ValueError: Si no es proporcionado alguno de los datos necesarios.
            - ErrorConsejoPlantaNoExiste: Si el consejo del la planta de esa zona y tipo de medida especificados no existe

        Returns:
            - Sensor: Registro creado del sensor.
        """
        if descripcion is None:
            raise ValueError('Necesario especificar la descripcion de los consejos de la planta.')
        if nombre_planta is None:
            raise ValueError('Necesario especificar la planta a la que se aplicaran los consejos.')
        if zona_consejo is None:
            raise ValueError('Necesario especificar la zona en la que se aplicaran los consejos de la planta.')
        if tipo_medida is None:
            raise ValueError('Necesario especificar el tipo de medida de los consejos de la planta.')
        if unidad_medida is None:
            raise ValueError('Necesario especificar la unidad de medida de los consejos de la planta.')
        if valor_minimo is None:
            raise ValueError('Necesario especificar el valor minimo del consejo de la planta.')
        if valor_maximo is None:
            raise ValueError('Necesario especificar el valor maximo del consejo de la planta.')

        consejo_modificado = None
        try:
            query = session.query(ConsejoPlanta).filter_by(nombre_elemento=nombre_planta, zona_consejo=zona_consejo, tipo_medida=tipo_medida)
            consejo: ConsejoPlanta = query.one()
            if consejo.descripcion != descripcion:
                query.update({'descripcion' : descripcion})
            if consejo.unidad_medida != unidad_medida:
                query.update({'unidad_medida' : unidad_medida})
            if consejo.valor_minimo != valor_minimo:
                query.update({'valor_minimo' : valor_minimo})
            if consejo.valor_maximo != valor_maximo:
                query.update({'valor_maximo' : valor_maximo})
            if consejo.horas_minimas != horas_minimas:
                query.update({'horas_minimas' : horas_minimas})
            if consejo.horas_maximas != horas_maximas:
                query.update({'horas_maximas' : horas_maximas})
            session.commit()
            consejo_modificado: ConsejoPlanta = query.one() 
        except NoResultFound as ex:
            raise ErrorConsejoPlantaNoExiste(
                'El consejo de la planta ' + str(nombre_planta) + ' para la medida ' + str(tipo_medida) +
                ' en la zona ' + str(zona_consejo) + ' ya está registrado.'
                ) from ex
        finally:
            return consejo_modificado
        
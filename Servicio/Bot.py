from Modelo.Configuracion import Configuracion
from Servicio.Log import Log
from Servicio.ServiciosAter import ServiciosAter
from Servicio.ServiciosSalesfoce import ServiciosSalesforce
from Servicio.ServiciosTerminales import ServiciosTerminales


class Bot:
    def __init__(self):
        self._estado = True
        self._configuracion = None
        self._datos_ater = {}
        self._datos_salsforce = {}
        self._terminales = {}


    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def configuracion(self):
        return self._configuracion

    @configuracion.setter
    def configuracion(self, configuracion):
        self._configuracion = configuracion

    @property
    def datos_ater(self):
        return self._datos_ater

    @datos_ater.setter
    def datos_ater(self, datos_ater):
        self._datos_ater = datos_ater

    @property
    def datos_salesforce(self):
        return self._datos_salesforce

    @datos_salesforce.setter
    def datos_salesforce(self, datos_salesforce):
        self._datos_salesforce = datos_salesforce

    @property
    def terminales(self):
        return self._terminales

    @terminales.setter
    def terminales(self, terminales):
        self._terminales = terminales

    def iniciar(self):
        status_code = 0
        log = Log()
        try:
            log.verificar_archivo_log()
            mensaje = f" {'='*128 }"
            log.escribir(mensaje, tiempo=False)
            mensaje = f"Iniciando Bot Salesforce Sync State..."
            log.escribir(mensaje)
            mensaje = f" {'~'*128 }"
            log.escribir(mensaje, tiempo=False)

            configuracion = Configuracion(log)
            configuracion.cargar()
            self.configuracion = configuracion
            self.estado = self.configuracion.bot.estado
            if not self.estado:
                mensaje = f"Bot apagado por configuracion..."
                log.escribir(mensaje)
                return

            servicios_ater = ServiciosAter(log, self.configuracion)
            self.datos_ater = servicios_ater.buscarterminales()
            if self.datos_ater is False:
                return

            servicios_salesforce = ServiciosSalesforce(log, self.configuracion)
            self.datos_salesforce = servicios_salesforce.buscarterminales()
            if self.datos_salesforce is False:
                return

            servicios_terminales = ServiciosTerminales(log, self.datos_ater, self.datos_salesforce)
            self.terminales = servicios_terminales.filtrar()
            if self.terminales is False:
                return

        except Exception as excepcion:
            status_code = 1
            mensaje = f" {'-'*128 }"
            log.escribir(mensaje, tiempo=False)
            mensaje = f"ERROR - Ejecucion principal: {str(excepcion)}"
            log.escribir(mensaje)
        finally:
            if not self.estado:
                mensaje = f" {'-' * 128}"
                log.escribir(mensaje, tiempo=False)
                mensaje = f"WARNING!!! - Proceso principal interrumpido, no se realizaran mas acciones..."
                log.escribir(mensaje)

            mensaje = f" {'~' * 128}"
            log.escribir(mensaje, tiempo=False)
            mensaje = f"Finalizando Bot Salesforce Sync State..."
            log.escribir(mensaje)
            mensaje = f" {'='*128 }"
            log.escribir(mensaje, tiempo=False)
            log.cerrar()
            del log
            return status_code

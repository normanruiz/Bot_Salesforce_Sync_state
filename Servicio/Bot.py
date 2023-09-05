from Modelo.Configuracion import Configuracion
from Servicio.Log import Log
from Servicio.ServiciosAter import ServiciosAter
from Servicio.ServiciosReporte import ServiciosReporte
from Servicio.ServiciosSalesfoce import ServiciosSalesforce
from Servicio.ServiciosTerminales import ServiciosTerminales


class Bot:
    def __init__(self):
        self._estado = True
        self._log = None
        self._configuracion = None
        self._datos_ater = {}
        self._datos_salesforce = {}

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, log):
        self._log = log

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

    def iniciar(self):
        status_code = 0
        self.log = Log()
        try:
            self.log.verificar_archivo_log()
            mensaje = f" {'='*128 }"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"Iniciando Bot Salesforce Sync State..."
            self.log.escribir(mensaje)
            mensaje = f" {'~'*128 }"
            self.log.escribir(mensaje, tiempo=False)

            configuracion = Configuracion(self.log)
            self.estado = configuracion.cargar()
            self.configuracion = configuracion
            if self.estado is False:
                return

            self.estado = self.configuracion.bot.estado
            if not self.estado:
                mensaje = f"Bot apagado por configuracion..."
                self.log.escribir(mensaje)
                return

            servicios_ater = ServiciosAter(self.log, self.configuracion)
            self.datos_ater = servicios_ater.buscarterminales()
            if self.datos_ater is False:
                return

            servicios_salesforce = ServiciosSalesforce(self.log, self.configuracion)
            self.datos_salesforce = servicios_salesforce.buscarterminales()
            if self.datos_salesforce is False:
                return

            servicios_terminales = ServiciosTerminales(self.log, self.datos_ater, self.datos_salesforce)
            self.estado = servicios_terminales.filtrar()
            if self.estado is False:
                return

            self.estado = servicios_ater.actualizarterminales(servicios_terminales.terminales_estado_11)
            if self.estado is False:
                return

            self.estado = servicios_salesforce.actualizarterminales(servicios_terminales.terminales_estado_0)
            if self.estado is False:
                return

            servicios_reporte = ServiciosReporte(self.log, self.configuracion)
            self.estado = servicios_reporte.generar_reporte(servicios_terminales.terminales_estado_10, servicios_terminales.terminales_estado_11, servicios_salesforce.terminales_salesforce_ok, servicios_salesforce.terminales_salesforce_fail, servicios_terminales.terminales_fail_merchant, servicios_terminales.terminales_estado_none, servicios_terminales.terminales_fail)
            if self.estado is False:
                return

        except Exception as excepcion:
            status_code = 1
            mensaje = f" {'-'*128 }"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"ERROR - Ejecucion principal: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            if not self.estado:
                mensaje = f" {'-' * 128}"
                self.log.escribir(mensaje, tiempo=False)
                mensaje = f"WARNING!!! - Proceso principal interrumpido, no se realizaran mas acciones..."
                self.log.escribir(mensaje)

            mensaje = f" {'~' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"Finalizando Bot Salesforce Sync State..."
            self.log.escribir(mensaje)
            mensaje = f" {'='*128 }"
            self.log.escribir(mensaje, tiempo=False)
            self.log.cerrar()
            return status_code

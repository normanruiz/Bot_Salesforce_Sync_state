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
        self._terminales = {}
        self._terminales_salesforce_ok = []
        self._terminales_salesforce_fail = []

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

    @property
    def terminales(self):
        return self._terminales

    @terminales.setter
    def terminales(self, terminales):
        self._terminales = terminales

    @property
    def terminales_salesforce_ok(self):
        return self._terminales_salesforce_ok

    @terminales_salesforce_ok.setter
    def terminales_salesforce_ok(self, terminales_salesforce_ok):
        self._terminales_salesforce_ok = terminales_salesforce_ok

    @property
    def terminales_salesforce_fail(self):
        return self._terminales_salesforce_fail

    @terminales_salesforce_fail.setter
    def terminales_salesforce_fail(self, terminales_salesforce_fail):
        self._terminales_salesforce_fail = terminales_salesforce_fail

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
            if self.datos_salesforce is False:
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
            self.terminales = servicios_terminales.filtrar()
            if self.terminales is False:
                return

            self.estado = servicios_ater.actualizarterminales(servicios_terminales.filtrar_estado(11))
            if self.estado is False:
                return

            self.estado, self._terminales_salesforce_ok, self._terminales_salesforce_fail = servicios_salesforce.actualizarterminales(servicios_terminales.filtrar_estado(0))
            if self.estado is False:
                return

            servicios_reporte = ServiciosReporte(self.log, self.configuracion)
            self.estado = servicios_reporte.generar_reporte(servicios_terminales.filtrar_estado(10), servicios_terminales.filtrar_estado(11), self._terminales_salesforce_ok, self._terminales_salesforce_fail, servicios_terminales.filtrar_estado(None), servicios_terminales.filtrar_estado('invalido'), servicios_terminales.terminales_fail_merchant)
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

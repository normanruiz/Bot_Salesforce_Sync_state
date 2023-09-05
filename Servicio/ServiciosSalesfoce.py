from Modelo.Terminal import Terminal
from Servicio.ConexionAPI import ConexionAPI


class ServiciosSalesforce:
    def __init__(self, log, configuracion):
        self._log = log
        self._configuracion = configuracion
        self._terminales = {}
        self._terminales_update = {}
        self._terminales_salesforce_ok = []
        self._terminales_salesforce_fail = []

    @property
    def log(self):
        return self._log

    @property
    def configuracion(self):
        return self._configuracion

    @property
    def terminales(self):
        return self._terminales

    @terminales.setter
    def terminales(self, terminales):
        self._terminales = terminales

    @property
    def terminales_update(self):
        return self._terminales_update

    @terminales_update.setter
    def terminales_update(self, terminales_update):
        self._terminales_update = terminales_update

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

    def buscarterminales(self):
        estado = True
        datos = {}
        try:
            mensaje = f"Recuperando datos de Salesforce..."
            self.log.escribir(mensaje)

            datos_api = self.configuracion.conexiones[1]
            api_salesforce = ConexionAPI(self.log)
            api_salesforce.autenticarse(datos_api)
            datos_respuesta = api_salesforce.consultar()
            if datos_respuesta is False:
                raise Exception('Fallo la recoleccion de datos.')
            else:
                for numero, estado in datos_respuesta.items():
                    terminal = Terminal()
                    terminal.numero = numero
                    terminal.estado = estado
                    datos[terminal.numero] = terminal
            self.terminales = datos

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Recuperando datos de Salesforce: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            if estado is False:
                return False
            else:
                return self.terminales

    def actualizarterminales(self, terminales):
        estado = True
        self.terminales_update = terminales
        try:
            mensaje = f"Actualizando terminales con estado 0 en salesforce..."
            self.log.escribir(mensaje)

            if len(self.terminales_update) > 0:
                file_datos_csv = 'Externalid__c,FS_Estado_migracion__c,FS_Merchant__c\n'
                for numero, terminal in self.terminales_update.items():
                    file_datos_csv += f"{terminal.numero},10,{terminal.merchant}\n"
                datos_api = self.configuracion.conexiones[1]
                api_salesforce = ConexionAPI(self.log)
                api_salesforce.autenticarse(datos_api)
                estado, self.terminales_salesforce_ok, self.terminales_salesforce_fail = api_salesforce.actualizar(file_datos_csv)
            else:
                mensaje = f"Lote vacio, no hay terminales para actualizar..."
                self.log.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"Error - Actualizando terminales con estado 0 en salesforce: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            return estado
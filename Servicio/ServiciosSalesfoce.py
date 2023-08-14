from Servicio.ConexionAPI import ConexionAPI


class ServiciosSalesforce:
    def __init__(self, log, configuracion):
        self._log = log
        self._configuracion = configuracion
        self.terminales = {}

    @property
    def log(self):
        return self._log

    @property
    def configuracion(self):
        return self._configuracion

    def buscarterminales(self):
        estado = True
        try:
            mensaje = f"Recuperando datos de Salesforce..."
            self.log.escribir(mensaje)

            datos_api = self.configuracion.conexiones[1]
            api_salesforce = ConexionAPI(self.log)
            api_salesforce.autenticarse(datos_api)
            self.terminales = api_salesforce.consultar()

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Recuperando datos de Ater: {str(excepcion)}"
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

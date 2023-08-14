
class ServiciosTerminales:
    def __init__(self, log, datos_ater=None, datos_salesforce=None):
        self._log = log
        self._datos_ater = datos_ater
        self._datos_salesforce = datos_salesforce
        self._terminales = {}

    @property
    def log(self):
        return self._log

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

    def filtrar(self):
        estado = True
        estado_0 = 0
        estado_10 = 0
        estado_11 = 0
        informar = 0
        try:
            mensaje = f"Procesando terminales..."
            self.log.escribir(mensaje)

            self.terminales = self.datos_ater
            for numero, terminal in self.terminales.items():
                if terminal.estado == 0:
                    estado_0 += 1
                elif terminal.estado == 10:
                    estado_10 += 1
                elif terminal.estado == 11:
                    estado_11 += 1
                else:
                    informar += 1
                if numero in self.datos_salesforce.keys():
                    self.terminales[numero].estado = self.datos_salesforce[numero].estado
                else:
                    self.terminales[numero].estado = None

            mensaje = f"Terminales detectadas con estado 0: {estado_0}"
            self.log.escribir(mensaje)
            mensaje = f"Terminales detectadas con estado 10: {estado_10}"
            self.log.escribir(mensaje)
            mensaje = f"Terminales detectadas con estado 11: {estado_11}"
            self.log.escribir(mensaje)
            mensaje = f"Terminales detectadas con algun fallo: {informar}"
            self.log.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Procesando terminales: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            return estado


class ServiciosTerminales:
    def __init__(self, log, datos_ater=None, datos_salesforce=None):
        self._log = log
        self._datos_ater = datos_ater
        self._datos_salesforce = datos_salesforce
        self._terminales = {}
        self._terminales_estado_0 = {}
        self._terminales_estado_10 = {}
        self._terminales_estado_11 = {}
        self._terminales_estado_none = {}
        self._terminales_fail = {}
        self._terminales_fail_merchant = {}

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

    @property
    def terminales_estado_0(self):
        return self._terminales_estado_0

    @terminales_estado_0.setter
    def terminales_estado_0(self, terminales_estado_0):
        self._terminales_estado_0 = terminales_estado_0

    @property
    def terminales_estado_10(self):
        return self._terminales_estado_10

    @terminales_estado_10.setter
    def terminales_estado_10(self, terminales_estado_10):
        self._terminales_estado_10 = terminales_estado_10

    @property
    def terminales_estado_11(self):
        return self._terminales_estado_11

    @terminales_estado_11.setter
    def terminales_estado_11(self, terminales_estado_11):
        self._terminales_estado_11 = terminales_estado_11

    @property
    def terminales_estado_none(self):
        return self._terminales_estado_none

    @terminales_estado_none.setter
    def terminales_estado_none(self, terminales_estado_none):
        self._terminales_estado_none = terminales_estado_none
    @property
    def terminales_fail(self):
        return self._terminales_fail

    @terminales_fail.setter
    def terminales_fail(self, terminales_fail):
        self._terminales_fail = terminales_fail

    @property
    def terminales_fail_merchant(self):
        return self._terminales_fail_merchant

    @terminales_fail_merchant.setter
    def terminales_fail_merchant(self, terminales_fail_merchant):
        self._terminales_fail_merchant = terminales_fail_merchant

    def filtrar(self):
        estado = True
        try:
            mensaje = f"Procesando terminales..."
            self.log.escribir(mensaje)

            self.terminales = self.datos_ater
            for numero, terminal in self.terminales.items():
                if numero in self.datos_salesforce.keys():
                    self.terminales[numero].estado = self.datos_salesforce[numero].estado
                else:
                    self.terminales[numero].estado = None

            for numero, terminal in self.terminales.items():
                if terminal.estado == 0:
                    if terminal.merchant in ['-1', None]:
                        self.terminales_fail_merchant[numero] = terminal
                    else:
                        self.terminales_estado_0[numero] = terminal
                elif terminal.estado == 10:
                    self.terminales_estado_10[numero] = terminal
                elif terminal.estado == 11:
                    self.terminales_estado_11[numero] = terminal
                elif terminal.estado is None:
                    self.terminales_estado_none[numero] = terminal
                else:
                    self.terminales_fail[numero] = terminal

            mensaje = f"Terminales detectadas con estado 0: {len(self.terminales_estado_0)}"
            self.log.escribir(mensaje)
            mensaje = f"Terminales detectadas con estado 10: {len(self.terminales_estado_10)}"
            self.log.escribir(mensaje)
            mensaje = f"Terminales detectadas con estado 11: {len(self.terminales_estado_11)}"
            self.log.escribir(mensaje)
            mensaje = f"Terminales detectadas con algun fallo: {len(self.terminales_estado_none) + len(self.terminales_fail_merchant)}"
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

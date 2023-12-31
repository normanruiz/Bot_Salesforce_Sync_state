class Terminal:
    def __init__(self, numero=None, estado=None, merchant=None):
        self._numero = numero
        self._estado = estado
        self._merchant = merchant

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        if estado == '0':
            self._estado = 0
        elif estado == '11':
            self._estado = 11
        elif estado == '10':
            self._estado = 10
        else:
            self._estado = estado

    @property
    def merchant(self):
        return self._merchant

    @merchant.setter
    def merchant(self, merchant):
        self._merchant = merchant

    def to_update_ater(self):
        return (11, self.numero)

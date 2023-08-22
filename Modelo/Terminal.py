class Terminal:
    def __init__(self, numero=None, estado=None):
        self._numero = numero
        self._estado = estado

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

    def to_update(self):
        return (self.estado, self.numero)

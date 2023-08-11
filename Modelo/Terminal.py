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
        self._estado = estado

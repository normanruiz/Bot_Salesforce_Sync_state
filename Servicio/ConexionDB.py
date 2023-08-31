import pyodbc


class ConexionDB:
    def __init__(self, log):
        self._log = log
        self._conexion = None
        self._database = None

    @property
    def log(self):
        return self._log

    @property
    def conexion(self):
        return self._conexion

    @conexion.setter
    def conexion(self, conexion):
        self._conexion = conexion

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    def conectar(self, driver, server, database, usuario, contrasenia):
        estado = True
        self.database = database
        try:
            mensaje = f"Conectando a base de datos {database}..."
            self.log.escribir(mensaje)
            cadena_de_conexion = f'DRIVER={driver};' \
                                 f'SERVER={server};' \
                                 f'DATABASE={database};' \
                                 f'UID={usuario};' \
                                 f'PWD={contrasenia};' \
                                 f'TrustServerCertificate=yes;'
            self.conexion = pyodbc.connect(cadena_de_conexion)
            mensaje = f"Conexion establecida con base de datos {database}..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Conectando a base de datos {database}: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

    def desconectar(self):
        estado = True
        try:
            mensaje = f"Cerrando conexion con base de datos {self.database}..."
            self.log.escribir(mensaje)

            self.conexion.close()

            mensaje = f"Conexion a base de datos {self.database} cerrada..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cerrando conexion a base de datos {self.database}: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

    def ejecutar_select(self, consulta):
        estado = True
        data = []
        cursor = None
        try:
            mensaje = f"Ejecutando query contra {self.database}..."
            self.log.escribir(mensaje)
            mensaje = f"Query: {consulta}"
            self.log.escribir(mensaje)
            mensaje = f"Generando cursor..."
            self.log.escribir(mensaje)
            cursor = self.conexion.cursor()
            mensaje = f"Comenzando lectura de datos..."
            self.log.escribir(mensaje)

            cursor.execute(consulta)
            data = cursor.fetchall()

            mensaje = f"Lectura de datos finalizada..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Ejecutando query: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            if cursor:
                cursor.close()
                mensaje = f"Destruyendo cursor..."
                self.log.escribir(mensaje)
            return data if estado else estado

    def ejecutar_update(self, consulta, datos):
        estado = True
        cursor = None
        try:
            mensaje = f"Ejecutando update contra {self.database}..."
            self.log.escribir(mensaje)
            mensaje = f"Query: {consulta}"
            self.log.escribir(mensaje)
            mensaje = f"Generando cursor..."
            self.log.escribir(mensaje)
            conexion = self.conexion
            cursor = conexion.cursor()
            mensaje = f"Comenzando escritura de datos..."
            self.log.escribir(mensaje)

            cursor.fast_executemany = True
            cursor.executemany(consulta, datos)
            conexion.commit()
            mensaje = f"Total de registros actualizados: {len(datos)}"
            self.log.escribir(mensaje)

            mensaje = f"Escritura de datos finalizada..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Ejecutando update: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            if cursor:
                cursor.close()
                mensaje = f"Destruyendo cursor..."
                self.log.escribir(mensaje)
            return estado

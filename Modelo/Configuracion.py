import xmltodict


class Configuracion:
    def __init__(self, log):
        self._log = log
        self._configfile = 'config.xml'
        self._bot = None
        self._conexiones = []

    @property
    def log(self):
        return self._log

    @property
    def configfile(self):
        return self._configfile

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    @property
    def conexiones(self):
        return self._conexiones

    @conexiones.setter
    def conexiones(self, conexiones):
        self._conexiones = conexiones

    def cargar(self):
        estado = True
        try:
            mensaje = f"Cargando configuracion..."
            self.log.escribir(mensaje)
            with open(self._configfile, 'r', encoding='utf8') as xmlfile:
                xmlconfig = xmlfile.read()
                config = xmltodict.parse(xmlconfig)
            autor = Autor(config["parametros"]["bot"]["autor"]["nombre"],
                          config["parametros"]["bot"]["autor"]["correo"])
            bot = Bot(config["parametros"]["bot"]["nombre"],
                      True if config["parametros"]["bot"]["estado"] == 'True' else False,
                      int(config["parametros"]["bot"]["hilos"]), autor)
            self.bot = bot
            conexion_db = Conexion(config["parametros"]["conexiones_db"]["driver"],
                                   config["parametros"]["conexiones_db"]["server"],
                                   config["parametros"]["conexiones_db"]["database"],
                                   config["parametros"]["conexiones_db"]["username"],
                                   config["parametros"]["conexiones_db"]["password"],
                                   config["parametros"]["conexiones_db"]["select_terminales"],
                                   config["parametros"]["conexiones_db"]["select_merchants"],
                                   config["parametros"]["conexiones_db"]["update"])
            self.conexiones.append(conexion_db)
            api_salesforce = ApiSalesforce(config["parametros"]["api_salesforce"]["org"],
                                 config["parametros"]["api_salesforce"]["client_id"],
                                 config["parametros"]["api_salesforce"]["client_secret"],
                                 config["parametros"]["api_salesforce"]["username"],
                                 config["parametros"]["api_salesforce"]["password"],
                                 config["parametros"]["api_salesforce"]["version"],
                                 config["parametros"]["api_salesforce"]["select"])
            self.conexiones.append(api_salesforce)
            api_teams = ApiTeams(config["parametros"]["api_teams"]["asunto"],
                                 config["parametros"]["api_teams"]["remitente"],
                                 config["parametros"]["api_teams"]["destinatario"],
                                 config["parametros"]["api_teams"]["ip"],
                                 config["parametros"]["api_teams"]["port"])
            self.conexiones.append(api_teams)
            mensaje = f"Configuracion cargada correctamente..."
            self.log.escribir(mensaje)
            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cargando configuracion: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            return estado


class Autor:
    def __init__(self, nombre=None, correo=None):
        self._nombre = nombre
        self._correo = correo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, correo):
        self._correo = correo


class Bot:
    def __init__(self, nombre=None, estado=None, hilos=None, autor=None):
        self._nombre = nombre
        self._estado = estado
        self._hilos = hilos
        self._autor = autor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def hilos(self):
        return self.hilos

    @hilos.setter
    def hilos(self, hilos):
        self._hilos = hilos

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, autor):
        self._autor = autor


class Conexion:
    def __init__(self, driver, server, database, username, password, select_terminales, select_merchants, update):
        self._driver = driver
        self._server = server
        self._database = database
        self._username = username
        self._password = password
        self._select_terminales = select_terminales
        self._select_merchants = select_merchants
        self._update = update

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        self._server = server

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def select_terminales(self):
        return self._select_terminales

    @select_terminales.setter
    def select_terminales(self, select_terminales):
        self._select_terminales = select_terminales

    @property
    def select_merchants(self):
        return self._select_merchants

    @select_merchants.setter
    def select_merchants(self, select_merchants):
        self._select_merchants = select_merchants

    @property
    def update(self):
        return self._update

    @update.setter
    def update(self, update):
        self._update = update

class ApiSalesforce:
    def __init__(self, org=None, client_id=None, client_secret=None, username=None, password=None, version=None, select=None):
        self._org = org
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        self._token = None
        self._instanceUrl = None
        self._version = version
        self._select = select

    @property
    def org(self):
        return self._org

    @org.setter
    def org(self, org):
        self._org = org

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id

    @property
    def client_secret(self):
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        self._client_secret = client_secret

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def instanceUrl(self):
        return self._instanceUrl

    @instanceUrl.setter
    def instanceUrl(self, instanceUrl):
        self._instanceUrl = instanceUrl

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, select):
        self._select = select

class ApiTeams:
    def __init__(self, asunto=None, remitente=None, destinatario=None, ip=None, port=None):
        self.asunto = asunto
        self._remitente = remitente
        self._destinatario = destinatario
        self._ip = ip
        self._port = port

    @property
    def asunto(self):
        return self._asunto

    @asunto.setter
    def asunto(self, asunto):
        self._asunto = asunto

    @property
    def remitente(self):
        return self._remitente

    @remitente.setter
    def remitente(self, remitente):
        self._remitente = remitente

    @property
    def destinatario(self):
        return self._destinatario

    @destinatario.setter
    def destinatario(self, destinatario):
        self._destinatario = destinatario

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port
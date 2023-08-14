import json

import requests

from Modelo.Terminal import Terminal


class ConexionAPI:
    def __init__(self, log):
        self._log = log
        self._api = None

    @property
    def log(self):
        return self._log

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, api):
        self._api = api

    def autenticarse(self, api):
        estado = True
        self.api = api
        try:
            mensaje = f"Solicitando autenticacion..."
            self.log.escribir(mensaje)

            url = f"{self.api.org}/services/oauth2/token"
            payload = f"grant_type=password&" \
                      f"client_id={self.api.client_id}&" \
                      f"client_secret={self.api.client_secret}&" \
                      f"username={self.api.username}&" \
                      f"password={self.api.password}"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'BrowserId=bbfYdfx5EeyQbsWMygN5mw; CookieConsentPolicy=0:0; LSKey-c$CookieConsentPolicy=0:0'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            datos = json.loads(response.text)
            self.api.token = datos["access_token"]
            self.api.instanceUrl = datos["instance_url"]

            mensaje = f"Access token obtenido..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Solicitando autenticacion: {type(excepcion)} - {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

    def consultar(self):
        estado = True
        datos = {}
        try:
            mensaje = f"Consultando datos..."
            self.log.escribir(mensaje)

            url = f"{self.api.instanceUrl}/services/data/{self.api.version}/query/?q={self.api.select}"

            payload = {}
            headers = {
                'Authorization': f"Bearer {self.api.token}",
                'Cookie': 'BrowserId=Gug6ojh1Ee6d15VXoMqV4g; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            resultado = json.loads(response.text)

            for record in resultado["records"]:
                terminal = Terminal()
                terminal.numero = record["Externalid__c"]
                terminal.estado = record["FS_Estado_migracion__c"]
                datos[terminal.numero] = terminal

            mensaje = f"Datos obtenidos: {len(datos)} registros..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Consultando datos: {type(excepcion)} - {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return datos if estado else estado

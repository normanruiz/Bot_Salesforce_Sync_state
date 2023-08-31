import os
from datetime import date
import time
from email.message import EmailMessage
import smtplib


class ServiciosReporte:
    def __init__(self, log, configuracion):
        self._log = log
        self._configuracion = configuracion
        self._archivo = None

    @property
    def log(self):
        return self._log

    @property
    def configuracion(self):
        return self._configuracion

    @property
    def archivo(self):
        return self._archivo

    @archivo.setter
    def archivo(self, archivo):
        self._archivo = archivo

    def generar_reporte(self, terminales_omitidas, terminales_ater, terminales_salesforce_ok, terminales_salesforce_fail, terminales_inexistentes, terminales_invalidas):
        estado = True
        archivo = f"Reporte-{date.today()}"
        try:
            mensaje = f"Generando reporte..."
            self.log.escribir(mensaje)

            self.archivo = open(f"{archivo}.html", "w", encoding="utf8")
            self.archivo.write(f"<!DOCTYPE html>\n")
            self.archivo.write(f"<html lang=\"en\">\n")
            self.archivo.write(f"<head>\n")
            self.archivo.write(f"\t<meta charset=\"UTF-8\">\n")
            self.archivo.write(f"\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
            self.archivo.write(f"\t<title>Reporte {date.today()}</title>\n")

            self.archivo.write("\t<style type=\"text/css\" media=\"screen\">\n")
            self.archivo.write("\t\tbody{background-color: white;margin: 10px 60px;padding: 10px 60px;}\n")
            self.archivo.write("\t\th1{margin: 20px;padding: 20px;border: 2px solid blue;border-radius: 6px;box-shadow: 6px 6px 10px black;text-decoration: underline;}\n")
            self.archivo.write("\t\th2{display: inline-block;margin: 10px 20px;padding: 10px 20px;border: 2px solid;border-radius: 6px;box-shadow: 6px 6px 10px black;}\n")
            self.archivo.write("\t\th3{display: inline-block;margin: 10px 20px;padding: 10px 20px;border: 2px solid;border-radius: 6px;box-shadow: 6px 6px 10px black;}\n")
            self.archivo.write("\t\t#green{border-color: green;}\n")
            self.archivo.write("\t\t#red{border-color: red;}\n")
            self.archivo.write("\t\t#yellow{border-color: yellow;}\n")
            self.archivo.write("\t\t#orange{border-color: orange;}\n")
            self.archivo.write("\t\tp>i{margin: 10px 20px;padding: 10px 20px;}\n")
            self.archivo.write("\t\tp>b{margin: 10px 20px;padding: 10px 20px;}\n")
            self.archivo.write("\t\ttable{border: 2px solid lightgray;border-radius: 6px;margin: 10px 20px;padding: 10px 20px;border-spacing: 20px 10px;}\n")
            self.archivo.write("\t\ttd{padding: 6px 20px;border-radius: 4px;background-color: rgb(127,160,160);}\n")
            self.archivo.write("\t</style>\n")

            self.archivo.write(f"</head>\n")
            self.archivo.write(f"<body>\n")
            self.archivo.write(f"\t<hr><h1>Reporte Bot Salesforce Sync State</h1>\n")
            self.archivo.write(f"\t<p><i>Fecha: {date.today()} Hora: {time.strftime('%H:%M:%S', time.localtime())}</i></p><hr>\n")

            self.archivo.write(f"\t<h2 id=\"yellow\">Terminales omitidas con estado 10 en salesforce: {len(terminales_omitidas)}</h2>\n")
            if len(terminales_omitidas) == 0:
                self.archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
            else:
                self.archivo.write(f"\t<table>\n")
                self.archivo.write(f"\t\t<tbody>\n")
                self.archivo.write(f"\t\t\t<tr>\n")
                contador = 0
                for numero in terminales_omitidas:
                    if contador < 5:
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                        contador += 1
                    else:
                        self.archivo.write(f"\t\t\t</tr>\n")
                        contador = 1
                        self.archivo.write(f"\t\t\t<tr>\n")
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                else:
                    self.archivo.write(f"\t\t\t</tr>\n")
                self.archivo.write(f"\t\t</tbody>\n")
                self.archivo.write(f"\t</table>\n")

            self.archivo.write(f"\t<hr><h2 id=\"green\">Terminales actulizadas en Ater a estado 11: {len(terminales_ater)}</h2>\n")
            if len(terminales_ater) == 0:
                self.archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
            else:
                self.archivo.write(f"\t<table>\n")
                self.archivo.write(f"\t\t<tbody>\n")
                self.archivo.write(f"\t\t\t<tr>\n")
                contador = 0
                for numero in terminales_ater:
                    if contador < 5:
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                        contador += 1
                    else:
                        self.archivo.write(f"\t\t\t</tr>\n")
                        contador = 1
                        self.archivo.write(f"\t\t\t<tr>\n")
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                else:
                    self.archivo.write(f"\t\t\t</tr>\n")
                self.archivo.write(f"\t\t</tbody>\n")
                self.archivo.write(f"\t</table>\n")

            self.archivo.write(f"\t<hr><h2 id=\"orange\">Terminales actualizadas en Salesforce a estado 10: {len(terminales_salesforce_ok) + len(terminales_salesforce_fail)}</h2><br>\n")
            self.archivo.write(f"\t<h3 id=\"green\">Actualizacion Ok: {len(terminales_salesforce_ok)}</h3>\n")
            if len(terminales_salesforce_ok) == 0:
                self.archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
            else:
                self.archivo.write(f"\t<table>\n")
                self.archivo.write(f"\t\t<tbody>\n")
                self.archivo.write(f"\t\t\t<tr>\n")
                contador = 0
                for numero in terminales_salesforce_ok:
                    if contador < 5:
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                        contador += 1
                    else:
                        self.archivo.write(f"\t\t\t</tr>\n")
                        contador = 1
                        self.archivo.write(f"\t\t\t<tr>\n")
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                else:
                    self.archivo.write(f"\t\t\t</tr>\n")
                self.archivo.write(f"\t\t</tbody>\n")
                self.archivo.write(f"\t</table>\n")
            self.archivo.write(f"\t<h3 id=\"red\">Actualizacion fallida: {len(terminales_salesforce_fail)}</h3>\n")
            if len(terminales_salesforce_fail) == 0:
                self.archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
            else:
                self.archivo.write(f"\t<table>\n")
                self.archivo.write(f"\t\t<tbody>\n")
                self.archivo.write(f"\t\t\t<tr>\n")
                contador = 0
                for numero in terminales_salesforce_fail:
                    if contador < 5:
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                        contador += 1
                    else:
                        self.archivo.write(f"\t\t\t</tr>\n")
                        contador = 1
                        self.archivo.write(f"\t\t\t<tr>\n")
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                else:
                    self.archivo.write(f"\t\t\t</tr>\n")
                self.archivo.write(f"\t\t</tbody>\n")
                self.archivo.write(f"\t</table>\n")

            self.archivo.write(f"\t<hr><h2 id=\"orange\">Terminales con incidentes: {len(terminales_inexistentes) + len(terminales_invalidas)}</h2><br>\n")
            self.archivo.write(f"\t<h3 id=\"red\">Terminales inexistentes en Salesforce: {len(terminales_inexistentes)}</h3>\n")
            if len(terminales_inexistentes) == 0:
                self.archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
            else:
                self.archivo.write(f"\t<table>\n")
                self.archivo.write(f"\t\t<tbody>\n")
                self.archivo.write(f"\t\t\t<tr>\n")
                contador = 0
                for numero in terminales_inexistentes:
                    if contador < 5:
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                        contador += 1
                    else:
                        self.archivo.write(f"\t\t\t</tr>\n")
                        contador = 1
                        self.archivo.write(f"\t\t\t<tr>\n")
                        self.archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                else:
                    self.archivo.write(f"\t\t\t</tr>\n")
                self.archivo.write(f"\t\t</tbody>\n")
                self.archivo.write(f"\t</table>\n")
            self.archivo.write(f"\t<h3 id=\"red\">Terminales con estado invalido: {len(terminales_invalidas)}</h3>\n")
            if len(terminales_invalidas) == 0:
                self.archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
            else:
                self.archivo.write(f"\t<table>\n")

                self.archivo.write(f"\t\t<tbody>\n")
                self.archivo.write(f"\t\t\t<tr>\n")
                contador = 0
                for numero, terminal in terminales_invalidas.items():
                    if contador < 5:
                        self.archivo.write(f"\t\t\t\t<td>Terminal: {terminal.numero}</td> <td>Estado: {terminal.estado}</td>\n")
                        contador += 1
                    else:
                        self.archivo.write(f"\t\t\t</tr>\n")
                        contador = 1
                        self.archivo.write(f"\t\t\t<tr>\n")
                        self.archivo.write(f"\t\t\t\t<td>Terminal: {terminal.numero}</td> <td>Estado: {terminal.estado}</td>\n")
                else:
                    self.archivo.write(f"\t\t\t</tr>\n")
                self.archivo.write(f"\t\t</tbody>\n")
                self.archivo.write(f"\t</table><hr>\n")

            msg = EmailMessage()
            msg['Subject'] = self.configuracion.conexiones[2].subject
            msg['From'] = self.configuracion.conexiones[2].de
            msg['To'] = self.configuracion.conexiones[2].to
            msg.set_content(f"", subtype='html')
            msg.add_attachment(
                self.archivo.read(),
                filename=f"{archivo}.html",
                maintype="application",
                subtype="html"
            )
            s = smtplib.SMTP(self.configuracion.conexiones[2].ip, self.configuracion.conexiones[2].port)
            s.send_message(msg)
            s.quit()

            self.archivo.close()

            # os.remove(f"{archivo}.html")

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Generando reporte: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

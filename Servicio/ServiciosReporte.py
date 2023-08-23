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

    def generar_reporte(self, terminales_omitidas, terminales_ater, terminales_salesforce, terminales_inexistentes, terminales_invalidas):
        estado = True
        archivo = f"Reporte-{date.today()}"
        try:
            mensaje = f"Generando reporte..."
            self.log.escribir(mensaje)


            self.archivo = open(f"{archivo}.md" , "w", encoding="utf8")
            self.archivo.write(f"# Reporte Bot Salesforce Sync State\n")
            self.archivo.write(f"\n*Fecha: {date.today()} Hora: {time.strftime('%H:%M:%S', time.localtime())}*\n")

            self.archivo.write(f"\n## Terminales omitidas con estado 10 en salesforce\n\n")
            if len(terminales_omitidas) == 0:
                self.archivo.write(f"\tNo se detectaron termianles en este estadio.\n")
            else:
                contador = 0
                for numero, terminal in terminales_omitidas.items():
                    if contador < 5:
                        self.archivo.write(f"\t{terminal.numero}")
                        contador += 1
                    else:
                        contador = 1
                        self.archivo.write(f"\n")
                        self.archivo.write(f"\t{terminal.numero}")
                else:
                    self.archivo.write(f"\n")

            self.archivo.write(f"\n## Terminales actulizadas en Ater a estado 11\n\n")
            if len(terminales_ater) == 0:
                self.archivo.write(f"\tNo se detectaron termianles en este estadio.\n")
            else:
                contador = 0
                for terminal in terminales_ater:
                    if contador < 5:
                        self.archivo.write(f"\t{terminal.numero}")
                        contador += 1
                    else:
                        contador = 1
                        self.archivo.write(f"\n")
                        self.archivo.write(f"\t{terminal.numero}")
                else:
                    self.archivo.write(f"\n")

            self.archivo.write(f"\n## Terminales actualizadas en Salesforce a estado 10\n\n")
            if len(terminales_salesforce) == 0:
                self.archivo.write(f"\tNo se detectaron termianles en este estadio.\n")
            else:
                contador = 0
                for numero, terminal in terminales_salesforce.items():
                    if contador < 5:
                        self.archivo.write(f"\t{terminal.numero}")
                        contador += 1
                    else:
                        contador = 1
                        self.archivo.write(f"\n")
                        self.archivo.write(f"\t{terminal.numero}")
                else:
                    self.archivo.write(f"\n")

            self.archivo.write(f"\n## Terminales con incidentes\n")

            self.archivo.write(f"\n### Terminales inexistentes en Salesforce\n\n")
            if len(terminales_inexistentes) == 0:
                self.archivo.write(f"\tNo se detectaron termianles en este estadio.\n")
            else:
                contador = 0
                for numero, terminal in terminales_inexistentes.items():
                    if contador < 5:
                        self.archivo.write(f"\t{terminal.numero}")
                        contador += 1
                    else:
                        contador = 1
                        self.archivo.write(f"\n")
                        self.archivo.write(f"\t{terminal.numero}")
                else:
                    self.archivo.write(f"\n")

            self.archivo.write(f"\n### Terminales con estado invalido\n\n")
            if len(terminales_invalidas) == 0:
                self.archivo.write(f"\tNo se detectaron termianles en este estadio.\n")
            else:
                contador = 0
                self.archivo.write(f"| Terminal | Estado | Termianl | Estado | Termianl | Estado |\n")
                self.archivo.write(f"| -- | -- | -- | -- | -- | -- |\n | ")
                for numero, terminal in terminales_invalidas.items():
                    if contador < 3:
                        self.archivo.write(f" {terminal.numero} | {terminal.estado} |")
                        contador += 1
                    else:
                        contador = 1
                        self.archivo.write(f"\n")
                        self.archivo.write(f"\t{terminal.numero}")
                else:
                    self.archivo.write(f"\n")

            os.system(f"mdpdf -o {archivo}.pdf {archivo}.md")

            msg = EmailMessage()
            msg['Subject'] = self.configuracion.conexiones[2].subject
            msg['From'] = self.configuracion.conexiones[2].de
            msg['To'] = self.configuracion.conexiones[2].to
            msg.set_content(f"", subtype='html')
            msg.add_attachment(
                self.archivo.read(),
                filename=f"{archivo}.pdf",
                maintype="application",
                subtype="pdf"
            )
            s = smtplib.SMTP(self.configuracion.conexiones[2].ip, self.configuracion.conexiones[2].port)
            s.send_message(msg)
            s.quit()

            self.archivo.close()
            os.remove(f"{archivo}.md")
            os.remove(f"{archivo}.pdf")

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Generando reporte: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

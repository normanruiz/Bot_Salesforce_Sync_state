import os
from datetime import date
import time


class Log:
    def __init__(self):
        fecha = str(date.today())
        self._carpeta_log = os.path.join(".", "files_log")
        self._archivo_log = f"log-{fecha}.txt"
        self._filename = os.path.join(self._carpeta_log, self._archivo_log)
        self._file_log = None

    @property
    def carpeta_log(self):
        return self._carpeta_log

    @property
    def archivo_log(self):
        return self._archivo_log

    @property
    def file_log(self):
        return self._file_log

    @file_log.setter
    def file_log(self, file_log):
        self._file_log = file_log

    def verificar_archivo_log(self):
        estado = True
        try:
            if not os.path.exists(self.carpeta_log):
                os.mkdir(self.carpeta_log)
            if not os.path.exists(os.path.join(self.carpeta_log, self.archivo_log)):
                self.file_log = open(os.path.join(self.carpeta_log, self.archivo_log), "w", encoding="utf8")
                self.file_log.write(" " + "=" * 128 + "\n")
                self.file_log.write(
                    f"  {str(date.today())} {time.strftime('%H:%M:%S', time.localtime())} - Archivo de log generado\n")
            else:
                self.file_log = open(os.path.join(self.carpeta_log, self.archivo_log), "a", encoding="utf8")
        except Exception as excepcion:
            estado = False
            print(f"  Error - Fallo la verificacion del archivo de logs: {str(excepcion)}")
        finally:
            return estado

    def escribir(self, mensaje, tiempo=True, archivo=True, pantalla=True):
        estado = True
        hora = time.strftime('%H:%M:%S', time.localtime())
        registro = ''
        try:
            if tiempo:
                registro += f"  {hora} {mensaje}"
            else:
                registro += f"{mensaje}"
            if pantalla:
                print(registro)
            if archivo:
                self.file_log.write(f"{registro}\n")
        except Exception as excepcion:
            estado = False
            print("  ERROR - Escribiendo log:", str(excepcion))
        finally:
            return estado

    def cerrar(self):
        estado = True
        try:
            self.file_log.close()
        except Exception as excepcion:
            estado = False
            print("  ERROR - Cerrando el archivo de logs:", str(excepcion))
        finally:
            return estado

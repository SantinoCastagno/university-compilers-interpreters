# -*- coding: utf-8 -*-

# Importa los módulos necesarios
import os
import sys

def construir_lexema(fuente):
    lexema = "lexema "
    while caracter:
        if not (caracter == " " or caracter == "\t" or caracter == "\n"):
            if (caracter.isAlpha()):
                lexema += caracter
                caracter = fuente.read(1)
                while (caracter.isalpha or caracter.isdigit):
                    lexema += caracter
                    caracter = fuente.read(1)
                lexema += ", token(ident, puntero a ts)"
                    return lexema
            elif (caracter==";"):
                lexema += caracter + "token(puntoComa, null)"
                return lexema
            elif (caracter=="."):
                lexema += caracter + "token(punto, null)"
                return lexema
            elif (caracter==":"):
                caracter = fuente.read(1)
                if (caracter == "="):
                    lexema += caracter + "token(asignacion, null)"
                    return lexema
                lexema += caracter + "token(dosPuntos, null)"
                return lexema
            elif (caracter=="<"):
                if 

        caracter = fuente.read(1)

def leer_fuente(ruta):
    try:
        with open(ruta, 'r') as fuente:
            caracter = fuente.read(1)
            while caracter:
                lexema = construir_lexema(fuente)
                print(lexema)
                caracter = fuente.read(1)
    except FileNotFoundError:
        print("El fuente no existe o no se pudo abrir.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_del_archivo>")
        sys.exit(1)

    ruta_archivo = sys.argv[1]
    leer_archivo(ruta_archivo)

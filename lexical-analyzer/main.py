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
                return lexema + ", token(ident, puntero-a-ts)"
            elif (caracter==";"):
                lexema += caracter 
                return lexema + ", token(puntoComa, null)"
            elif (caracter=="."):
                lexema += caracter 
                return lexema + ", token(punto, null)"
            elif (caracter==":"):
                lexema += caracter
                caracter = fuente.read(1)
                if (caracter == "="):
                    lexema += caracter + ", token(asignacion, null)"
                    return lexema
                lexema += caracter + ", token(dosPuntos, null)"
                return lexema
            elif (caracter ==","):
                lexema += caracter
                return lexema + ", token(coma, null)"
            elif (caracter =="<"):
                lexema += caracter
                caracter = fuente.read(1)
                if (caracter == "="):
                    lexema += caracter 
                    return lexema + ", token(asignacion, menorIgual)"
                elif (caracter == ">"):
                    lexema += caracter 
                    return lexema + ", token(operadorRelacional, distinto)"
                return lexema + ", token(operadorRelacional, menor)"
            elif (caracter == ">"):
                lexema += caracter
                caracter = fuente.read(1)
                if (caracter == "="):
                    lexema += caracter
                    return lexema + ", token(operadorRelacional, mayorIgual)"
                return lexema + ", token(operadorRelacional, mayor)"
            elif (caracter == "+"):
                lexema += caracter
                return lexema + "token(operadorAritmetico, suma)"
            elif (caracter == "-"):
                lexema += caracter
                return lexema + "token(operadorAritmetico, resta)"
            elif (caracter == "{"):
                lexema += caracter
                while (caracter.isdigit or caracter.isalpha or caracter == " " or caracter == "\t" or caracter == "\n"):
                    lexema += caracter
                    caracter = fuente.read(1)
                if (caracter == "}"):
                    lexema += caracter 
                    caracter = fuente.read(1)
                    return "token(null, null)"
                else:
                    return "Error: digit not recognized."
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

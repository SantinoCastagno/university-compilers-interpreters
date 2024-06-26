# -*- coding: utf-8 -*-

import os
import sys

keyword_list = ["program", "begin", "if", "else", "then", "while", "end", "and", "or", "var", "procedure", "function", "do", "integer", "boolean"]
boolean_list = ["true", "false"]

caracter = " "

def construir_lexema(fuente):
    global caracter
    lexema = "lexema "
    while caracter:
        if not (caracter == " " or caracter == "\t" or caracter == "\n"):
            if (caracter.isalpha()): 
                lexema += caracter
                palabra = caracter
                caracter = fuente.read(1)
                while (caracter.isalpha() or caracter.isdigit()):
                    palabra += caracter
                    lexema += caracter
                    if (palabra in boolean_list):
                        if palabra == "true":
                            return lexema + ", token('booleanDato', 'trueValor')"
                        else:
                            return lexema + ", token('booleanDato', 'falseValor')"
                    caracter = fuente.read(1)
                if (palabra in keyword_list):
                    return lexema + ", token('keyword', '" + palabra + "')"
                return lexema + ", token('id', 'id')"
            elif (caracter.isdigit()):
                numero = str(caracter)
                caracter = fuente.read(1)
                while (caracter.isdigit()):
                    numero += str(caracter)
                    caracter = fuente.read(1)
                return lexema + numero + ", token('enteroDato','"+ numero + "')"
            elif (caracter==";"):
                lexema += caracter 
                caracter = fuente.read(1)
                return lexema + ", token('puntoComa', None)"
            elif (caracter=="."):
                lexema += caracter 
                caracter = fuente.read(1)
                return lexema + ", token('punto', None)"
            elif (caracter==":"):
                lexema += caracter
                caracter = fuente.read(1)
                if (caracter == "="):
                    lexema += caracter + ", token('asignacion', None)"
                    caracter = fuente.read(1)
                    return lexema
                lexema += ", token('dosPuntos', None)"
                return lexema
            elif (caracter ==","):
                lexema += caracter
                caracter = fuente.read(1)
                return lexema + ", token('coma', None)"
            elif (caracter =="<"):
                lexema += caracter
                caracter = fuente.read(1)
                if (caracter == "="):
                    lexema += caracter 
                    caracter = fuente.read(1)
                    return lexema + ", token('asignacion', '<=')"
                elif (caracter == ">"):
                    lexema += caracter 
                    caracter = fuente.read(1)
                    return lexema + ", token('operadorRelacional', '<>')"
                caracter = fuente.read(1)
                return lexema + ", token('operadorRelacional', '<')"
            elif (caracter == ">"):
                lexema += caracter
                caracter = fuente.read(1)
                if (caracter == "="):
                    lexema += caracter
                    caracter = fuente.read(1)
                    return lexema + ", token('operadorRelacional', '>=')"
                caracter = fuente.read(1)
                return lexema + ", token('operadorRelacional', '>')"
            elif (caracter == "+"):
                lexema += caracter
                caracter = fuente.read(1)
                return lexema + ", token('operadorAritmetico', '+')"
            elif (caracter == "-"):
                lexema += caracter
                caracter = fuente.read(1)
                return lexema + ", token('operadorAritmetico', '-')"
            elif (caracter == "*"):
                lexema += caracter
                caracter = fuente.read(1)
                return lexema + ", token('operadorAritmetico', '*')"
            elif (caracter == "/"):
                lexema += caracter
                caracter = fuente.read(1)
                return lexema + ", token('operadorAritmetico', '/')"
            elif (caracter == "("):
                lexema += caracter
                caracter = fuente.read(1)
                return lexema + ", token('parentesis', '(')"
            elif (caracter == ")"):
                lexema += caracter
                caracter = fuente.read(1)
                return lexema + ", token('parentesis', ')')"
            elif (caracter == "{"):
                lexema += caracter
                caracter = fuente.read(1)
                while (caracter != "}"):
                    lexema += caracter
                    caracter = fuente.read(1)
                lexema += caracter 
                caracter = fuente.read(1)
                return ""
            elif (caracter == "'"):
                lexema += caracter
                caracter = fuente.read(1)
                while (caracter != "'"):
                    lexema += caracter
                    caracter = fuente.read(1)
                lexema += caracter 
                caracter = fuente.read(1)
                return ""
            print("Error: digit not recognized:"+ caracter)        
        caracter = fuente.read(1)

def leer_fuente(ruta_fuente, ruta_destino):#
    global caracter
    try:
        with open(ruta_fuente, 'r') as fuente:
            try:
                with open(ruta_destino, 'w') as destino:
                    while caracter:
                        lexema = construir_lexema(fuente)
                        if (lexema ):
                            destino.write(lexema + "\n")
                        else:
                            print("Finalizacion del analisis lexico.")
            except IOError:
                 print("Error al escribir en el archivo destino.")
    except FileNotFoundError:
        print("El fuente no existe o no se pudo abrir.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <ruta_del_fuente_origen> <ruta_del_archivo_destino")
        sys.exit(1)
    ruta_fuente = sys.argv[1]
    ruta_destino = sys.argv[2]
    leer_fuente(ruta_fuente, ruta_destino)

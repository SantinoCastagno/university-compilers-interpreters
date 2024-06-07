# -*- coding: utf-8 -*-

import os
import sys

keyword_list = ["program", "begin", "if", "else", "then", "while", "end", "and", "or", "var", "procedure", "function", "do", "integer", "boolean"]
boolean_list = ["true", "false"]

caracter = " "
row = 1
col = 1

def construir_lexema(fuente):
    global caracter, row, col
    lexema = "lexema "
    while caracter:
        if not (caracter == " " or caracter == "\t" or caracter == "\n"):
            if (caracter.isalpha()): 
                lexema += caracter
                palabra = caracter
                caracter = fuente.read(1)
                col = col + 1
                while (caracter.isalpha() or caracter.isdigit()):
                    palabra += caracter
                    lexema += caracter
                    if (palabra in boolean_list):
                        if palabra == "true":
                            return lexema + ", token('booleanDato', 'trueValor')"
                        else:
                            return lexema + ", token('booleanDato', 'falseValor')"
                    caracter = fuente.read(1)
                    col = col + 1
                if (palabra in keyword_list):
                    return lexema + ", token('keyword', '" + palabra + "')"
                return lexema + ", token('id', 'id')"
            elif (caracter.isdigit()):
                numero = str(caracter)
                caracter = fuente.read(1)
                col = col + 1
                while (caracter.isdigit()):
                    numero += str(caracter)
                    caracter = fuente.read(1)
                    col = col + 1
                return lexema + numero + ", token('enteroDato','"+ numero + "')"
            elif (caracter==";"):
                lexema += caracter 
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('puntoComa', None)"
            elif (caracter=="."):
                lexema += caracter 
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('punto', None)"
            elif (caracter==":"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                if (caracter == "="):
                    lexema += caracter + ", token('asignacion', None)"
                    caracter = fuente.read(1)
                    col = col + 1
                    return lexema
                lexema += ", token('dosPuntos', None)"
                return lexema
            elif (caracter ==","):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('coma', None)"
            elif (caracter =="="):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('operadorRelacional', '=')"
            elif (caracter =="<"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                if (caracter == "="):
                    lexema += caracter 
                    caracter = fuente.read(1)
                    col = col + 1
                    return lexema + ", token('asignacion', '<=')"
                elif (caracter == ">"):
                    lexema += caracter 
                    caracter = fuente.read(1)
                    col = col + 1
                    return lexema + ", token('operadorRelacional', '<>')"
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('operadorRelacional', '<')"
            elif (caracter == ">"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                if (caracter == "="):
                    lexema += caracter
                    caracter = fuente.read(1)
                    col = col + 1
                    return lexema + ", token('operadorRelacional', '>=')"
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('operadorRelacional', '>')"
            elif (caracter == "+"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('operadorAritmetico', '+')"
            elif (caracter == "-"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('operadorAritmetico', '-')"
            elif (caracter == "*"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('operadorAritmetico', '*')"
            elif (caracter == "/"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('operadorAritmetico', '/')"
            elif (caracter == "("):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('parentesis', '(')"
            elif (caracter == ")"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                return lexema + ", token('parentesis', ')')"
            elif (caracter == "{"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                while (caracter != "}"):
                    lexema += caracter
                    caracter = fuente.read(1)
                    col = col + 1
                lexema += caracter 
                caracter = fuente.read(1)
                col = col + 1
                return ""
            elif (caracter == "'"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                while (caracter != "'"):
                    lexema += caracter
                    caracter = fuente.read(1)
                    col = col + 1
                lexema += caracter 
                caracter = fuente.read(1)
                col = col + 1
                return ""
            else:
                print("Error: caracter no reconocido:"+ caracter)
        elif (caracter == " " or caracter == "\t"):       
            col = col + 1
        elif (caracter == "\n"):
            col = 1
            row = row + 1
        caracter = fuente.read(1)

def obtener_siguiente_token(fuente):
    while caracter:
        token = construir_lexema(fuente)
        if (token):
            return token;
        
def obtener_posicion():
    global row, col
    return row, col

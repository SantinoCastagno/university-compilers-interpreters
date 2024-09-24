# -*- coding: utf-8 -*-

import os
import sys

keyword_list = ["program", "begin", "if", "else", "then", "while", "end", "var", "procedure", "function", "do", "integer", "boolean", "AND", "OR"]
boolean_list = ["TRUE", "FALSE"]

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
                    caracter = fuente.read(1)
                    if (palabra in boolean_list):
                        if palabra == "TRUE":
                            return lexema + ", token('booleanDato', 'TRUE')"
                        else:
                            return lexema + ", token('booleanDato', 'FALSE')"
                    col = col + 1
                if (palabra in keyword_list):
                    return lexema + ", token('keyword', '" + palabra + "')"
                return lexema + ", token('id', '"+ lexema[7:] +"')"

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
                return lexema + ", token('operadorRelacionalIndividual', '=')"
            elif (caracter =="<"):
                lexema += caracter
                caracter = fuente.read(1)
                col = col + 1
                if (caracter == "="):
                    lexema += caracter 
                    caracter = fuente.read(1)
                    col = col + 1
                    return lexema + ", token('operadorRelacional', '<=')"
                elif (caracter == ">"):
                    lexema += caracter 
                    caracter = fuente.read(1)
                    col = col + 1
                    return lexema + ", token('operadorRelacionalIndividual', '<>')"
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
                print("\t\tfila:"+str(row)+"\tcolumna:"+str(col))
                sys,exit(1)
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

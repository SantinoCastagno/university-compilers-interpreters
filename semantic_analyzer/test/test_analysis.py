import subprocess
import pytest

@pytest.mark.parametrize("ruta_programa, salida_esperada", [
    ('./files/Ej01A1.PAS', 'SUCCESS  | error semantico: mismo identificador de variable global y programa\nSUCCESS  | fila:3 columna:12\n'),
    ('./files/Ej01A2.PAS', 'SUCCESS  | error semantico: mismo identificador de procedimiento y programa\nSUCCESS  | fila:5 columna:17'),
    ('./files/Ej01B1.PAS', 'SUCCESS  | error semantico: mismo identificador de procedimiento y variable global\nSUCCESS  | fila:12 columna:16\n'),
    ('./files/EJ01A3.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion y programa\nSUCCESS  | fila:5 columna:16\n'),
    ('./files/EJ01B1.PAS', 'SUCCESS  | error semantico: dos variables globales con el mismo nombre\nSUCCESS  | fila:4 columna:4\n'),
    ('./files/Ej01C.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion y variable global\nSUCCESS  | fila:6 columna:15\n'),
    ('./files/EJ01D.PAS', 'SUCCESS  | error semantico: mismo identificador de procedimiento y variable global\nSUCCESS  | fila:12 columna:16\n'),
    ('./files/EJ01E.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion local y variable local\nSUCCESS  | fila:14 columna:12\n'),
    ('./files/EJ01F.PAS', 'SUCCESS  | error semantico: mismo identificador de variable local y parametro local\nSUCCESS  | fila:12 columna:7\n'),
    ('./files/EJ01G.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion local y parametro local\nSUCCESS  | fila:14 columna:12\n'),
    ('./files/EJ01H.PAS', 'SUCCESS  | error semantico: mismo identificador de procedimiento local y parametro local\nSUCCESS  | fila:14 columna:13\n'),
    
    ('./files/EJ02A1.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    ('./files/EJ02A2.PAS', 'SUCCESS  | error semantico: identificador de variable sin definir\nSUCCESS  | fila:8 columna:13\n'),
    ('./files/EJ02A3.PAS', 'SUCCESS  | error semantico: identificador de funcion sin definir en expresion aritmetica\nSUCCESS  | fila:13 columna:15\n'),
    ('./files/EJ02A4.PAS', 'SUCCESS  | error semantico: identificador de funcion sin definir en expresion condicional\nSUCCESS  | fila:14 columna:13\n'),
    ('./files/EJ02A5.PAS', 'SUCCESS  | error semantico: identificador de funcion sin definir en expresion repetitiva\nSUCCESS  | fila:14 columna:13\n'),
    
    # ('./files/EJ03A1.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03A2.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03A.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03B1.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03B2.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03C1.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03C2.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03C3.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03D1.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03D2.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03E1.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
    # ('./files/EJ03E2.PAS', 'SUCCESS  | error semantico: identificador de procedimiento sin definir\nSUCCESS  | fila:13 columna:8\n'),
])
def test_program(ruta_programa, salida_esperada):
    result = subprocess.run(['python3', '../src/syntactic_analyzer.py', ruta_programa, 'SUCCESS'], capture_output=True, text=True)
    assert result.stdout == salida_esperada
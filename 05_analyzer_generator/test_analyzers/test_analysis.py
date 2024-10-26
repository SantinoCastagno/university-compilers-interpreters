import subprocess
import pytest

@pytest.mark.parametrize("ruta_programa, salida_esperada", [
    ('./files/Ej01A1.PAS', 'SUCCESS  | error semantico: mismo identificador de variable global y programa [prueba]\nSUCCESS  | fila:3 columna:12\n'),
    ('./files/Ej01A2.PAS', 'SUCCESS  | error semantico: mismo identificador de procedimiento y programa [prueba]\nSUCCESS  | fila:5 columna:17\n'),
    ('./files/Ej01A3.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion y programa [prueba]\nSUCCESS  | fila:5 columna:16\n'),
    ('./files/Ej01B1.PAS', 'SUCCESS  | error semantico: dos variables global con el mismo nombre [b]\nSUCCESS  | fila:4 columna:4\n'),
    ('./files/Ej01B2.PAS', 'SUCCESS  | error semantico: dos variables local con el mismo nombre [m]\nSUCCESS  | fila:7 columna:6\n'),
    ('./files/Ej01C.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion y variable global [nuevo]\nSUCCESS  | fila:6 columna:15\n'),
    ('./files/EJ01D.PAS', 'SUCCESS  | error semantico: mismo identificador de procedimiento y variable global [nuevo]\nSUCCESS  | fila:12 columna:16\n'),
    ('./files/EJ01E.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion local y variable local [j]\nSUCCESS  | fila:14 columna:12\n'),
    ('./files/EJ01F.PAS', 'SUCCESS  | error semantico: mismo identificador de variable local y parametro local [a]\nSUCCESS  | fila:12 columna:7\n'),
    ('./files/EJ01G.PAS', 'SUCCESS  | error semantico: mismo identificador de funcion local y parametro local [a]\nSUCCESS  | fila:14 columna:12\n'),
    ('./files/EJ01H.PAS', 'SUCCESS  | error semantico: mismo identificador de procedimiento local y parametro local [a]\nSUCCESS  | fila:14 columna:13\n'),
    
    ('./files/EJ02A1.PAS', 'SUCCESS  | error semantico: identificador de procedimiento [algo] sin definir \nSUCCESS  | fila:13 columna:8\n'),
    ('./files/EJ02A2.PAS', 'SUCCESS  | error semantico: identificador de variable [m] sin definir \nSUCCESS  | fila:8 columna:13\n'),
    ('./files/EJ02A3.PAS', 'SUCCESS  | error semantico: identificador de funcion [algo] sin definir en expresion aritmetica\nSUCCESS  | fila:13 columna:15\n'),
    ('./files/EJ02A4.PAS', 'SUCCESS  | error semantico: identificador de funcion [salida] sin definir en expresion condicional\nSUCCESS  | fila:14 columna:13\n'),
    ('./files/EJ02A5.PAS', 'SUCCESS  | error semantico: identificador de funcion [not] sin definir en expresion repetitiva\nSUCCESS  | fila:14 columna:13\n'),
    
    ('./files/EJ03A.PAS', 'SUCCESS  | error semantico: pasaje de 1 parametro/s de tipo integer a funcion [algo]. Se esperaba/n 0\nSUCCESS  | fila:17 columna:19\n'),
    ('./files/EJ03A1.PAS', 'SUCCESS  | error semantico: pasaje de 1 parametro/s de tipo boolean a funcion [algo]. Se esperaba/n 2 parametro/s de tipo boolean\nSUCCESS  | fila:18 columna:19\n'),
    ('./files/EJ03A2.PAS', 'SUCCESS  | error semantico: pasaje de 3 parametro/s de tipo boolean a funcion [algo]. Se esperaba/n 2 parametro/s de tipo boolean\nSUCCESS  | fila:18 columna:34\n'),
    ('./files/EJ03B1.PAS', 'SUCCESS  | error semantico: pasaje de 2 parametro/s de tipo integer a procedimiento [nuevo]. Se esperaba/n 3 parametro/s de tipo integer\nSUCCESS  | fila:19 columna:19\n'),
    ('./files/EJ03B2.PAS', 'SUCCESS  | error semantico: pasaje de 4 parametro/s de tipo integer a procedimiento [nuevo]. Se esperaba/n 3 parametro/s de tipo integer\nSUCCESS  | fila:19 columna:23\n'),
    ('./files/EJ03C1.PAS', 'SUCCESS  | error semantico: pasaje de 1 parametro/s de tipo boolean y 1 parametro/s de tipo integer a funcion [algo]. Se esperaba/n 2 parametro/s de tipo boolean\nSUCCESS  | fila:18 columna:21\n'),
    ('./files/EJ03C2.PAS', 'SUCCESS  | error semantico: pasaje de 1 parametro/s de tipo integer y 1 parametro/s de tipo boolean a funcion [algo]. Se esperaba/n 2 parametro/s de tipo boolean\nSUCCESS  | fila:18 columna:21\n'),
    ('./files/EJ03C3.PAS', 'SUCCESS  | error semantico: pasaje de 1 parametro/s de tipo integer y 1 parametro/s de tipo boolean a procedimiento [nuevo]. Se esperaba/n 2 parametro/s de tipo integer\nSUCCESS  | fila:19 columna:17\n'),
    ('./files/EJ03D1.PAS', 'SUCCESS  | error semantico: pasaje de 1 parametro/s de tipo boolean y 1 parametro/s de tipo integer a funcion [algo]. Se esperaba/n 2 parametro/s de tipo boolean\nSUCCESS  | fila:18 columna:27\n'),
    ('./files/EJ03D2.PAS', 'SUCCESS  | error semantico: pasaje de 1 parametro/s de tipo integer y 1 parametro/s de tipo boolean a procedimiento [nuevo]. Se esperaba/n 2 parametro/s de tipo integer\nSUCCESS  | fila:19 columna:23\n'),
    
    # TODO: agregar test sobre expresiones
    
    ('./files/EJ05A1.PAS', 'SUCCESS  | error semantico: funcion integer [algo] sin retorno.\nSUCCESS  | fila:10 columna:5\n'),
    ('./files/EJ05A2.PAS', 'SUCCESS  | error semantico: funcion integer [algo] sin retorno.\nSUCCESS  | fila:11 columna:6\n'),
    ('./files/EJ05B1.PAS', 'SUCCESS  | error semantico: variable de retorno boolean [algo] de funcion usada en expresion\nSUCCESS  | fila:9 columna:26\n'),
    ('./files/EJ05B2.PAS', 'SUCCESS  | error semantico: variable de retorno integer [algo] de funcion usada en expresion\nSUCCESS  | fila:10 columna:17\n'),
    ('./files/EJ05C1.PAS', 'SUCCESS  | error semantico: el tipo de retorno [integer] y el valor de la expresion [boolean] no coinciden.\nSUCCESS  | fila:10 columna:5\n'),
    
   
])
def test_program(ruta_programa, salida_esperada):
    result = subprocess.run(['python3', '../src/syntactic_analyzer.py', ruta_programa, 'SUCCESS'], capture_output=True, text=True)
    assert result.stdout == salida_esperada
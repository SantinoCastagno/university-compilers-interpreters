from loguru import logger

from pila import Pila

ruta_destino = None
gen_cantidad_variables_declaradas = 0 # cantidad de las variables declaradas del programa/subprograma actual, utilizada para reservar el espacio de memoria
gen_nivel_lexico_procedimiento = 0

expresion_a_posfijo = ""
codigo = {
    '+':'SUMA',
    '-':'SUST',
    '*':'MULT',
    '/':'DIVI',
    'and':'CONJ',
    'or':'DISJ',
    '<':'CMME',
    '>':'CMMA',
    '=':'CMIG',
    '<>':'CMDG',
    '<=':'CMNI',
    '>=':'CMYI'
}

contador_etiquetas_saltos = 0

def _gen_abrir_archivo():
    global ruta_destino
    try:
        with open(ruta_destino, 'w', encoding='utf-8') as archivo:
            archivo.write("")
    except Exception as e:
        logger.error(f"Ocurrió un error al crear el archivo: {e}")

def gen_generar_codigo(contenido_1, contenido_2 = "", etiqueta_l = ""):
    global ruta_destino
    try:
        with open(ruta_destino, 'a', encoding='utf-8') as archivo:
            archivo.write(f"{etiqueta_l}\t\t{contenido_1}\t{contenido_2}\n")
    except Exception as e:
        logger.error(f"Ocurrió un error al escribir el archivo: {e}")

def gen_iniciar_generador(ruta):
    global ruta_destino
    ruta_destino = ruta
    _gen_abrir_archivo()


def gen_infijo_a_posfijo(expression):
    precedence = {
        '<': 4, '<=': 4, '>': 4, '>=': 4, '=': 4, '<>': 4,
        'or': 5, 'and': 6,
        '+': 7, '-': 7, '*': 8, '/': 8
    }
    output = []
    stack = []

    for char in expression.split():

        if (char.isalnum() and char not in ['or','and']) :  # Si es un operando (número o variable)
            output.append(char)
        elif char in precedence:  # Si es un operador
            while (stack and stack[-1] != '(' and
                   precedence[char] <= precedence[stack[-1]]):
                output.append(stack.pop())
            stack.append(char)

        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Elimina el '(' de la pila'''

    while stack:
        output.append(stack.pop())

    return ' '.join(output)

def gen_generar_codigos_expresion_posfija(expresion,pila_TLs:Pila):
    for elem in expresion.split():
        if elem in ['True','False'] or intable(elem):
            gen_generar_codigo('APCT',elem)
        elif elem in codigo.keys():
            gen_generar_codigo(codigo[elem])
        else:
            index,posicion = gen_get_nivel_lexico_y_posicion(elem,pila_TLs)
            gen_generar_codigo('APVL',str(index)+','+str(posicion))

def intable(valor):
    try:
        int(valor)
        return True
    except (ValueError, TypeError):
        return False

def gen_get_cont_etq_saltos():
    global contador_etiquetas_saltos
    contador_etiquetas_saltos += 1
    return contador_etiquetas_saltos

def gen_get_nivel_lexico_y_posicion(identificador_izquierda_instruccion,pila_TLs):
    id = identificador_izquierda_instruccion
    pila_invertida = reversed(pila_TLs.items)
    logger.error(id)
    ubicacion = -1
    index = -1
    for index,ts in enumerate(pila_invertida):
        ts = ts.tabla
        if id in ts.keys():
            index = len(pila_TLs.items) - 1 - index
            if (ts[id]['subatributo'] == "parametro"):
                # Se cuenta la cantidad de parametros de la TS
                cantidad_parametros = 0
                posicion = 0
                for index, key in enumerate(ts.keys()):
                    logger.error("elemento actual:"+key)
                    logger.error("posicion actual:"+str(index))
                    if ts[key]['subatributo'] == "parametro":
                        if key == id:
                            posicion = index + 1
                        cantidad_parametros = cantidad_parametros + 1
                logger.error("cantidad_parametros:"+str(cantidad_parametros))
                logger.error("posicion:"+str(posicion))
                ubicacion = -(cantidad_parametros + 3 - posicion)
            break

    return index,ubicacion
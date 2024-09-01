import inspect
import sys
import os
from lexical_analyzer import obtener_siguiente_token, obtener_posicion
from symbol_table import Tabla_simbolos
from pila import Pila
from loguru import logger


preanalisis = {'v':'','l':''}
pila_TLs = Pila()
identificador_a_verificar_a_futuro = ''

# Inicializador de logger
logger.remove()
logger.add(sys.stdout, level="DEBUG") # colocar el nivel deseado
# logger.add("debugging.log", level="DEBUG")  

def imprimirPosiciones():
    row, col = obtener_posicion()
    logger.info("fila:"+str(row)+"\tcolumna:"+str(col))
    sys.exit(1)
    
############################################################################################
############################## METODOS DEL ANALISIS SINTACTICO #############################
############################################################################################

def match(terminal):
    if(terminal == preanalisis['v']):
        siguiente_terminal()
    else:
        logger.info("error de sintaxis: se esperaba '",terminal,"', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def match_list(terminales):
    if(preanalisis['v'] in terminales):
        siguiente_terminal()
    else:
        logger.info("error de sintaxis: se esperaba ",terminales)
        imprimirPosiciones()


def en_primeros(simbolo):
    #logger.debug(simbolo)
    for primero in primeros[simbolo]:
        #logger.debug(preanalisis['v'],',',primero,'--',type(primero))
        if type(primero) == str and preanalisis['v'] == primero:
            return True
        elif callable(primero) and en_primeros(str(primero.__name__)):
            return True
    return False

def siguiente_terminal():
    preanalisis['v'] = obtener_siguiente_token(archivo)
    #logger.debug('SIGUIENTE LINEA: ',preanalisis['v'])
    if preanalisis['v'] == None:
        return
    preanalisis['v'] = preanalisis['v'][preanalisis['v'].find('token'):]
    preanalisis['v'] = eval(preanalisis['v'])
    logger.debug('SIGUIENTE TERMINAL:\tv:' + preanalisis['v'] + '\tl: ' + preanalisis['l'])

def token(arg0,arg1):
    tokens_basicos = {
        'puntoComa':';',
        'coma':',',
        'dosPuntos':':',
        'asignacion':':=',
        'punto':'.'
    }
    preanalisis['l'] = ''
    if (arg0 == 'keyword'
        #or arg0 == 'id'
        or arg0 == 'parentesis'
        or arg0 == 'operadorAritmetico'
        or arg0 == 'operadorRelacional'
        or arg0 == 'booleanDato'
        ):
        return arg1
    
    if arg0 == 'enteroDato':
        return arg0
    
    if arg0 == 'id':
        preanalisis['l'] = arg1
        return arg0
    
    if arg0 in tokens_basicos.keys():
        return tokens_basicos[arg0]
    
# PROGRAMAS Y BLOQUES
def programa(): # Primera funcion ejecutada
    if preanalisis['v'] == 'program':
        pila_TLs.apilar(Tabla_simbolos()) # Se apila la tabla del entorno global
        pila_TLs.ver_cima().insertar(nombre='write', atributo='procedimiento', tipo_scope='global')
        match("program");identificador2('programa');match(';');bloque("global");match('.')
    else:
        logger.info("error de sintaxis: se esperaba 'program', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def bloque(entorno):
    if en_primeros('declaraciones_variables_opcional') or en_primeros('declaraciones_subrutinas_opcional') or en_primeros('instruccion_compuesta'):
        declaraciones_variables_opcional();declaraciones_subrutinas_opcional();instruccion_compuesta(entorno)#;match('.')
    else:
        logger.info('error de sintaxis: no se ha declarado el inicio de la función principal del programa')
        imprimirPosiciones()

def declaraciones_variables_opcional():
    if en_primeros("declaraciones_variables"):
        declaraciones_variables()

def declaraciones_subrutinas_opcional():
    if en_primeros("declaraciones_subrutinas"):
        declaraciones_subrutinas()

# DECLARACIONES
def declaraciones_variables():
    if preanalisis['v'] =='var':
        match("var");declaracion_variable();match(';');declaraciones_variables_repetitivas()
    else:
        logger.info("error de sintaxis: se esperaba 'var', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def declaraciones_variables_repetitivas():
    #if preanalisis['v'] == 'var':
    if en_primeros('declaracion_variable'): 
         #match("var");
         declaracion_variable();match(';');declaraciones_variables_repetitivas()

def declaracion_variable():
    if en_primeros('lista_identificadores'):
        lista_identificadores('variable');match(':');tipo()
    else:
        logger.info("error de sintaxis: no se definieron las variables")
        imprimirPosiciones()

def tipo():
    if preanalisis['v'] == 'integer':
        match('integer')
    elif preanalisis['v'] == 'boolean':
        match('boolean')
    else:
        logger.info('error de sintaxis: solo se permite tipo integer o boolean')
        imprimirPosiciones()

def lista_identificadores(atributo):
    if en_primeros('identificador'):
        identificador2(atributo);lista_identificadores_repetitiva(atributo)
    else:
        logger.info('error de sintaxis: aca deberia ir un identificador')
        imprimirPosiciones()

def lista_identificadores_repetitiva(atributo):
    if preanalisis['v'] == ',':
        match(','),identificador2(atributo),lista_identificadores_repetitiva(atributo)

def declaraciones_subrutinas():
    if en_primeros('declaracion_procedimiento'):
        declaracion_procedimiento("procedimiento");match(";");declaraciones_subrutinas()
    elif en_primeros('declaracion_funcion'):
        declaracion_funcion("funcion");match(";");declaraciones_subrutinas()

def declaracion_procedimiento(entorno):
    if preanalisis['v'] == 'procedure':
        match('procedure');identificador2('procedimiento')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();match(';');bloque(entorno)#instruccion_compuesta()
        pila_TLs.desapilar()
    else:
        logger.debug("error de sintaxis: se esperaba 'procedure', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def declaracion_funcion():
    if preanalisis['v']=='function':
        match('function');identificador2('funcion')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();match(':');tipo();match(';');bloque()#instruccion_compuesta()
        pila_TLs.desapilar()
    else:
        logger.debug("error de sintaxis: se esperaba 'function', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def parametros_formales_opcional():
    if en_primeros('parametros_formales'):
        parametros_formales()

def parametros_formales():
    if preanalisis['v'] == '(':
        match('(');seccion_parametros_formales();parametros_formales_repetitiva();match(')')
    else:
        logger.debug("error de sintaxis: se esperaba '(', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def parametros_formales_repetitiva():
    if preanalisis['v'] == ';':
        match(';');seccion_parametros_formales();parametros_formales_repetitiva()

def seccion_parametros_formales():
    if en_primeros('lista_identificadores'):
        lista_identificadores('parametro');match(':');tipo()

# INSTRUCCIONES
def instruccion_compuesta(entorno):
    if preanalisis['v'] == 'begin':
        match('begin');instruccion(entorno);match(';');instruccion_compuesta_repetitiva(entorno);match('end')
    else:
        logger.debug("error de sintaxis: se esperaba 'begin', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def instruccion_compuesta_repetitiva(entorno):
    if en_primeros('instruccion'):
        instruccion(entorno);match(';');instruccion_compuesta_repetitiva(entorno)

def instruccion(entorno):
    if en_primeros('identificador'):
        identificador3();instruccion_aux(entorno)
    elif en_primeros('instruccion_compuesta'):
        instruccion_compuesta()
    elif en_primeros('instruccion_condicional'):
        instruccion_condicional()
    elif en_primeros('instruccion_repetitiva'):
        instruccion_repetitiva()
    else:
        logger.debug('error de sintaxis: no se encontro una instruccion valida')
        imprimirPosiciones()

def instruccion_aux(entorno):
    if en_primeros('asignacion'):
        asignacion(entorno="asignacion")
    elif en_primeros('llamada_procedimiento'):
        chequear_identificador_sin_definir('procedimiento', entorno)
        llamada_procedimiento(entorno="procedimiento")
    else:
        logger.debug('error de sintaxis: se esperaba una asignacion o la llamada a un procedimiento')
        imprimirPosiciones()

def asignacion(entorno):
    if preanalisis['v'] == ':=':
        match(':=');expresion("asignacion")
    else:
        logger.debug("error de sintaxis: se esperaba ':=', se encontro '",preanalisis['v'],"'")

def llamada_procedimiento(entorno):
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional(entorno)
    else:
        logger.debug("error de sintaxis: no se cumple la estructura para llamar un procedimiento")

def lista_expresiones_opcional(entorno):
    if preanalisis['v'] == '(':
        match('(');lista_expresiones_procedimiento(entorno);match(')')

def instruccion_condicional():
    if preanalisis['v'] == 'if':
        match('if');expresion(entorno='if');match('then');instruccion();else_opcional()
    else:
        logger.debug("error de sintaxis: se esperaba'if', se encontro '",preanalisis['v'],"'")

def else_opcional():
    if preanalisis['v'] == 'else':
        match('else');instruccion()   

def instruccion_repetitiva():
    if preanalisis['v'] == 'while':
        match('while');expresion();match('do');instruccion()
    else:
        logger.debug("error de sintaxis:  se esperaba 'while', se encontro '",preanalisis['v'],"'")

# EXPRESIONES
def lista_expresiones_procedimiento(entorno):
    if en_primeros('lista_expresiones'):
        lista_expresiones(entorno)
    #if en_primeros('identificador'):
   #     identificador();lista_expresiones_procedimiento_repetitiva()
   # elif preanalisis['v'] == 'enteroDato':
   #     numero();lista_expresiones_procedimiento_repetitiva()

def lista_expresiones(entorno):
    if en_primeros('expresion'):
        expresion(entorno);lista_expresiones_repetitiva()
    else:
        logger.debug('error de sintaxis: lista_expresiones()') 
        imprimirPosiciones()

def lista_expresiones_repetitiva():
    if preanalisis['v'] ==',':
        match(',');expresion();lista_expresiones_repetitiva()

def expresion(entorno):
    if en_primeros('expresion_simple'):
        expresion_simple(entorno);relacion_opcional()
    else:
        logger.debug('error de sintaxis: la expresion no se inicio de manera correcta')
        imprimirPosiciones()

def relacion_opcional():
    if en_primeros('relacion'):
        relacion();expresion_simple()

def relacion():
    # esta es una forma reducida de calcular el primero() y el match para cada elemento
    terminales = ['=','<>','<=','<','>','>=']
    if preanalisis['v'] in terminales:
        match_list(terminales)
    else:
        logger.debug("error de sintaxis: se esperaba un operrador relacional, sea '=','<>','<=','<','>' o '>='")
        imprimirPosiciones()

def expresion_simple(entorno):
    if en_primeros('mas_menos_opcional') or  en_primeros('termino'):
        mas_menos_opcional();termino(entorno);expresion_simple_repetitiva()
    else:
        logger.debug('error de sintaxis: se espera un termino valido.')
        imprimirPosiciones()


def mas_menos_opcional():
    terminales = ['+','-']
    if preanalisis['v'] in terminales:
        match_list(terminales)

def expresion_simple_repetitiva():
    if en_primeros('mas_menos_or') or  en_primeros('termino'):
        mas_menos_or();termino("while");expresion_simple_repetitiva()

def mas_menos_or():
    terminales = ['+','-','or']
    if preanalisis['v'] in terminales:
        match_list(terminales)
    else:
        logger.debug('error de sintaxis: se espera una operacion "+", "-" o "or"')
        imprimirPosiciones()

def termino(entorno):
    if en_primeros('factor'):
        factor(entorno);termino_repetitiva()
    else:
        logger.debug('error de sintaxis: se espera un factor valido')
        imprimirPosiciones()

def termino_repetitiva():
    if preanalisis['v'] == '*':
        match('*');factor();termino_repetitiva()
    elif preanalisis['v'] == '/':
        match('/');factor();termino_repetitiva()
    elif preanalisis['v'] == 'and':
        match('and');factor();termino_repetitiva()

def factor(entorno):
    if en_primeros('identificador'):
       identificador3();chequear_identificador_sin_definir('variable', entorno) # Esto no es necesariamiente una variable, hay que generalizar
       factor_opcional()
    elif en_primeros('numero'):
        numero()
    elif preanalisis['v'] == '(': 
        match('(');expresion();match(')')
    elif preanalisis['v'] == 'not':
        match('not');factor()
    else:
        logger.debug('error de sintaxis: se espera un factor valido')
        imprimirPosiciones()

def factor_opcional():
    if en_primeros('llamada_funcion'):
        llamada_funcion()

def llamada_funcion():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()
        
def numero():
    if preanalisis['v'] == 'enteroDato':
        siguiente_terminal()
    else:
        logger.info('error de sintaxis: numero()')
        imprimirPosiciones()
        
def identificador():
    reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
'(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'and' ,
'not']
    if preanalisis['v'] in reservadas:
        logger.debug('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
        imprimirPosiciones()
    else:
        siguiente_terminal()

def identificador2(atributo):
    reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
    '(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'and' ,
    'not']
    if preanalisis['v'] in reservadas:
        logger.debug('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
        imprimirPosiciones()
    else:
        tipoScope = asignar_scope(atributo)
        colision_nombres(atributo,tipoScope)
        pila_TLs.ver_cima().insertar(nombre=preanalisis['l'], atributo=atributo, tipo_scope=tipoScope)
        #logger.debug('pos: ' + str(pila_TLs.tamanio()) + '--' + str(pila_TLs.print_cima())) # se imprime la tabla de simbolos al tope de la pila
        siguiente_terminal()

def identificador3():
    reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
    '(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'and' ,
    'not']
    if preanalisis['v'] in reservadas:
        logger.info('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
        imprimirPosiciones()
    else:
        global identificador_a_verificar_a_futuro
        identificador_a_verificar_a_futuro=preanalisis['l']
        siguiente_terminal()

############################################################################################
############################## METODOS DEL ANALISIS SEMANTICO ##############################
############################################################################################
def chequear_identificador_sin_definir(atributo, entorno):
    id = identificador_a_verificar_a_futuro
    identificadorDetectado = False
    i = pila_TLs.tamanio()-1
    logger.debug("chequeando\t"+str(id))
    # se recorre la pila en orden inverso
    while i>0 and not identificadorDetectado:
        tabla = pila_TLs.items[i].tabla
        logger.debug(str(tabla))
        if id == "write" or id == "read": # tal vez esto hay que generalizarlo para mas funciones genericas
            identificadorDetectado = True
        if id in tabla.keys(): # chequea si el identificador esta en la tabla
            logger.debug(atributo +"\t\t"+ str(id) +str(tabla[id]))
            if (atributo == "variable" or atributo == "parametro") and (tabla[id]['atributo'] == "variable" or tabla[id]['atributo'] == "parametro"):
                identificadorDetectado = True
            elif (tabla[id]['atributo'] == atributo):
                identificadorDetectado = True
        i-=1
    if not identificadorDetectado:
        if atributo == "procedimiento":
            logger.info('error semantico: identificador de procedimiento sin definir')
        elif atributo == "funcion":
            logger.info("error semantico: uso de identificador de funcion booleana no definido en condicion  " + entorno)
        elif atributo == "variable":
            if pila_TLs.tamanio() >= 2:
                logger.info("error semantico: identificador de variable sin definir en entorno local " + entorno)
            elif pila_TLs.tamanio() < 2:
                logger.info("error semantico: identificador de variable sin definir en entorno global " + entorno) 
            else:
                logger.warning("condicion no controlada")
        imprimirPosiciones()
    return identificadorDetectado
        
def asignar_scope(atributo):
    '''Si el atributo es de tipo variable, se le asigna su respectivo scope'''
    tipoScope = None
    if atributo == 'variable':
        if(pila_TLs.tamanio() < 2):
            tipoScope = "global" 
        else:
            tipoScope = "local"
    elif atributo in ['funcion','procedimiento']:
         if(pila_TLs.tamanio() >= 2):
            tipoScope = "local"
    return tipoScope

def colision_nombres(atributo,tipoScope):
    l = preanalisis['l']
    if l in pila_TLs.print_cima().keys():
        tipoScope1 = '' if tipoScope is None else ' '+tipoScope
        tipoScope2 = ' '+pila_TLs.print_cima()[l]['tipo_scope'] if 'tipo_scope' in pila_TLs.print_cima()[l].keys() else ''

        if (pila_TLs.print_cima()[l]['atributo'] != atributo):
            logger.info('error semantico: mismo identificador de ' + atributo+tipoScope1 + ' y ' +pila_TLs.print_cima()[l]['atributo']+tipoScope2)
            imprimirPosiciones()
        else:
            logger.info('error semantico: dos ' + atributo + 's ' + pila_TLs.print_cima()[l]['tipo_scope'] + 'es con el mismo nombre')
            imprimirPosiciones() 
    
############################################################################################
############################## METODOS DE EJECUCION PRINCIPAL ##############################
############################################################################################
def abrir_archivo(archivo):
    """Abre el archivo y devuelve el objeto del archivo."""
    try:
        f = open(archivo, 'r', encoding='utf-8')
        return f
    except IOError:
        logger.debug("Error al abrir el archivo.")
        return None
    
def leer_siguiente_linea(f):
    """Lee la siguiente línea del archivo dado."""
    if f:
        linea = f.readline()
        if linea:
            return linea.strip()  # Elimina el salto de línea al final
        else:
            f.close()  # Cierra el archivo al llegar al final
            return None
    else:
        return None

if __name__ == "__main__":
    primeros = {       
        "programa": ["program"],
        "bloque":[declaraciones_variables_opcional,declaraciones_subrutinas_opcional,instruccion_compuesta],
        "declaraciones_variables_opcional": [declaraciones_variables,None],
        "declaraciones_subrutinas_opcional": [declaraciones_subrutinas,None],

        "declaraciones_variables":["var"],
        "declaraciones_variables_repetitiva":['var',None],
        "declaracion_variable":[lista_identificadores],
        "tipo": ["integer","boolean"],
        "lista_identificadores":[identificador],
        "lista_identificadores_repetitiva":[",",None],
        "declaraciones_subrutinas":[declaracion_procedimiento,declaracion_funcion,None],
        "declaracion_procedimiento":["procedure"],
        "declaracion_funcion":["function"],
        "parametros_formales_opcional":[parametros_formales,None],
        "parametros_formales":["("],
        "parametros_formales_repetitiva":[";",None],
        "seccion_parametros_formales":[lista_identificadores],

        "instruccion_compuesta":['begin'],
        'instruccion_compuesta_repetitiva':[instruccion,None],
        'instruccion':[identificador,instruccion_compuesta,instruccion_condicional,instruccion_repetitiva],
        'instruccion_aux':[asignacion,llamada_procedimiento],
        'asignacion':[':='],
        'llamada_procedimiento':[lista_expresiones_opcional],
        'lista_expresiones_opcional':['(',None],
        'instruccion_condicional':['if'],
        'else_opcional':['else',None],
        'instruccion_repetitiva':['while'],

        'lista_expresiones':[expresion],
        'lista_expresiones_repetitiva':[',',None],
        'expresion':[expresion_simple],
        'relacion':['=','<>','<=','<','>','>='],
        'expresion_simple':[mas_menos_opcional,termino],
        'mas_menos_opcional':['+','-',None],
        'expresion_simple_repetitiva':[mas_menos_or,termino,None],
        'mas_menos_or':['+','-','or',None],
        'termino':[factor],
        'termino_repetitiva':['*','/','and',None],
        'factor':[identificador,numero,'(','not'],
        'factor_opcional':[llamada_funcion,None],
        'llamada_funcion':[lista_expresiones_opcional],

        'identificador':['id','true','false'],
        'numero':['enteroDato']
    }

    if len(sys.argv) != 2:
        logger.debug("Utilizar: python main.py <ruta_del_fuente_origen>")
        sys.exit(1)
    
    global caracter

    ruta_fuente = sys.argv[1]
    #directorio = '../lexical-analyzer/output.out'
    archivo = abrir_archivo(ruta_fuente)
    siguiente_terminal()
    programa()
    logger.debug('analisis sintactico-lexico terminado, programa aceptado.')
   
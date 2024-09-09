import inspect
import sys
import os
from lexical_analyzer import obtener_siguiente_token, obtener_posicion
from symbol_table import Tabla_simbolos
from pila import Pila
from collections import Counter
from loguru import logger

logger.remove()
#logger.add(sys.stdout, level="DEBUG", format="{file}:{line} - {message}")
logger.add(sys.stdout, level="DEBUG")

preanalisis = {'v':'','l':''}
pila_TLs = Pila()

# MACROVARIABLES DE CONTROL SEMANTICO
ultimas_variables_declaradas = [] # lista de elementos que se utiliza para asignar el tipo de dato a las ultimas variables declaradas
identificador_a_verificar_a_futuro = ''
expresion_actual = '' # si la expresion actual a evaluar es aritmetica, condicional, repetitiva o ninguna (cadena vacia).
parametros = [] # cuando se declara/invoca una funcion o procedimiento con parametros, se llevara una lista de los mismos
subprograma_de_parametros_contados = '' # aca se guarda el nombre del subprograma cuyos parametros fueron listados, para acceder al mismo luego de listarlos 
tipo_parametros = ''

def imprimirPosiciones():
    row, col = obtener_posicion()
    logger.info("\t\tfila:"+str(row)+"\tcolumna:"+str(col))
    sys.exit(1)
    en

def m(terminal):
    if(terminal == preanalisis['v']):
        siguiente_terminal()
    else:
        logger.info("error de sintaxis: se esperaba '",terminal,"', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def m_list(terminales):
    if(preanalisis['v'] in terminales):
        siguiente_terminal()
    else:
        logger.info("error de sintaxis: se esperaba ",terminales)
        imprimirPosiciones()


def en_primeros(simbolo):
    #logger.info(simbolo)
    for primero in primeros[simbolo]:
        #logger.info(preanalisis['v'],',',primero,'--',type(primero))
        if type(primero) == str and preanalisis['v'] == primero:
            return True
        elif callable(primero) and en_primeros(str(primero.__name__)):
            return True
    return False

def siguiente_terminal():
    preanalisis['v'] = obtener_siguiente_token(archivo)
    logger.debug(f"{preanalisis['v']:<50}{preanalisis['l']:<20}")
    if preanalisis['v'] == None:
        return
    preanalisis['v'] = preanalisis['v'][preanalisis['v'].find('token'):]
    preanalisis['v'] = eval(preanalisis['v'])

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
    
def incializar_TL_global():
    pila_TLs.apilar(Tabla_simbolos()) # Se apila la tabla del entorno global
    
    # se inserta write como procedimiento
    pila_TLs.ver_cima().insertar(
        nombre='write',
        atributo='procedimiento',
        tipo_scope='global')
    # se insertan TRUE y FALSE como variables
    pila_TLs.ver_cima().insertar(
        nombre='TRUE',
        atributo='variable',
        tipo_scope='global'
    )
    pila_TLs.ver_cima().insertar(
        nombre='FALSE',
        atributo='variable',
        tipo_scope='global'
    )

# PROGRAMAS Y BLOQUES
def programa(): # Primera funcion ejecutada
    if preanalisis['v'] == 'program':
        incializar_TL_global()
        m("program");cargar_identificador('programa');m(';');bloque();m('.')
    else:
        en('programa()')
        logger.info("error de sintaxis: se esperaba 'program', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def bloque():
    if en_primeros('declaraciones_variables_opcional') or en_primeros('declaraciones_subrutinas_opcional') or en_primeros('instruccion_compuesta'):
        declaraciones_variables_opcional();declaraciones_subrutinas_opcional();instruccion_compuesta()#;m('.')
    else:
        en('bloque()')
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
        m("var");declaracion_variable();m(';');declaraciones_variables_repetitivas()
    else:
        en('declaraciones_variables()')
        logger.info("error de sintaxis: se esperaba 'var', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def declaraciones_variables_repetitivas():
    #if preanalisis['v'] == 'var':
    if en_primeros('declaracion_variable'): 
         #m("var");
         declaracion_variable();m(';');declaraciones_variables_repetitivas()

def declaracion_variable():
    if en_primeros('lista_identificadores'):
        lista_identificadores('variable','variable');m(':');tipo()
    else:
        en('declaracion_variable()')
        logger.info("error de sintaxis: no se definieron las variables")
        imprimirPosiciones()

def tipo(): 
    global ultimas_variables_declaradas
    if preanalisis['v'] == 'integer':
        m('integer')
        asignar_tipo_a_variables('integer')
    elif preanalisis['v'] == 'boolean':
        m('boolean')
        asignar_tipo_a_variables('boolean')
    else:
        en('tipo()')
        logger.info('error de sintaxis: solo se permite tipo integer o boolean')
        imprimirPosiciones()

def lista_identificadores(atributo,subatributo):
    if en_primeros('identificador'):
        cargar_identificador(atributo,subatributo);lista_identificadores_repetitiva(atributo,subatributo)
    else:
        en('lista_identificadores()')
        logger.info('error de sintaxis: aca deberia ir un identificador')
        imprimirPosiciones()

def lista_identificadores_repetitiva(atributo,subatributo):
    if preanalisis['v'] == ',':
        m(','),cargar_identificador(atributo,subatributo),lista_identificadores_repetitiva(atributo,subatributo)

def declaraciones_subrutinas():
    if en_primeros('declaracion_procedimiento'):
        declaracion_procedimiento();m(";");declaraciones_subrutinas()
    elif en_primeros('declaracion_funcion'):
        declaracion_funcion();m(";");declaraciones_subrutinas()

def declaracion_procedimiento():
    if preanalisis['v'] == 'procedure':
        m('procedure');cargar_identificador('procedimiento')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();m(';');bloque()#instruccion_compuesta()
        pila_TLs.desapilar()
    else:
        en('declaracion_procedimiento()')
        logger.info("error de sintaxis: se esperaba 'procedure', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def declaracion_funcion():
    if preanalisis['v']=='function':
        m('function');cargar_identificador('funcion')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();m(':');tipo();m(';');bloque()
        pila_TLs.desapilar()
    else:
        en('declaracion_funcion()')
        logger.info("error de sintaxis: se esperaba 'function', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def parametros_formales_opcional():
    if en_primeros('parametros_formales'):
        parametros_formales()
    actualizar_parametros_subprograma()



def parametros_formales():
    if preanalisis['v'] == '(':
        m('(');seccion_parametros_formales();parametros_formales_repetitiva();m(')')
    else:
        en('parametros_formales()')
        logger.info("error de sintaxis: se esperaba '(', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def parametros_formales_repetitiva():
    if preanalisis['v'] == ';':
        m(';');seccion_parametros_formales();parametros_formales_repetitiva()

def seccion_parametros_formales():
    global tipo_parametros
    if en_primeros('lista_identificadores'):
        lista_identificadores('variable','parametro');m(':');tipo_parametros=preanalisis['v'];tipo();

# INSTRUCCIONES
def instruccion_compuesta():
    if preanalisis['v'] == 'begin':
        m('begin');instruccion();m(';');instruccion_compuesta_repetitiva();m('end')
    else:
        en('instruccion_compuesta()')
        logger.info("error de sintaxis: se esperaba 'begin', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def instruccion_compuesta_repetitiva():
    if en_primeros('instruccion'):
        instruccion();m(';');instruccion_compuesta_repetitiva()

def instruccion():
    global expresion_actual
    if en_primeros('identificador'):
        guardar_nombre_subprograma_para_contar_parametros()
        guardar_identificador_a_verificar_a_futuro()
        instruccion_aux()
    elif en_primeros('instruccion_compuesta'):
        instruccion_compuesta()
    elif en_primeros('instruccion_condicional'):
        expresion_actual = 'condicional'
        instruccion_condicional()
    elif en_primeros('instruccion_repetitiva'):
        expresion_actual = 'repetitiva'
        instruccion_repetitiva()
    else:
        en('instruccion()')
        logger.info('error de sintaxis: no se encontro una instruccion valida')
        imprimirPosiciones()

def instruccion_aux():
    if en_primeros('asignacion'):
        asignacion()
    elif en_primeros('llamada_procedimiento'):
        identificador_sin_definir('procedimiento')
        llamada_procedimiento()
    else:
        en('instruccion_aux()')
        logger.info('error de sintaxis: se esperaba una asignacion o la llamada a un procedimiento')
        imprimirPosiciones()

def asignacion():
    if preanalisis['v'] == ':=':
        m(':=');expresion()
    else:
        en('asignacion()')
        logger.info("error de sintaxis: se esperaba ':=', se encontro '",preanalisis['v'],"'")

def llamada_procedimiento():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()
        error_aridad('procedimiento')
    else:
        en('llamada_procedimiento()')
        logger.info("error de sintaxis: no se cumple la estructura para llamar un procedimiento")

def lista_expresiones_opcional():
    if preanalisis['v'] == '(':
        m('(');lista_expresiones_procedimiento();m(')')

def instruccion_condicional():
    if preanalisis['v'] == 'if':
        m('if');expresion();m('then');instruccion();else_opcional()
    else:
        en('instruccion_condicional()')
        logger.info("error de sintaxis: se esperaba'if', se encontro '",preanalisis['v'],"'")

def else_opcional():
    if preanalisis['v'] == 'else':
        m('else');instruccion()   

def instruccion_repetitiva():
    if preanalisis['v'] == 'while':
        m('while');expresion();m('do');instruccion()
    else:
        en('error de sintaxis: else_opcional()')
        logger.info("error de sintaxis:  se esperaba 'while', se encontro '",preanalisis['v'],"'")

# EXPRESIONES
def lista_expresiones_procedimiento():
    if en_primeros('lista_expresiones'):
        lista_expresiones()
    #if en_primeros('identificador'):
   #     identificador();lista_expresiones_procedimiento_repetitiva()
   # elif preanalisis['v'] == 'enteroDato':
   #     numero();lista_expresiones_procedimiento_repetitiva()

def lista_expresiones():
    if en_primeros('expresion'):
        sumar_parametro_actual();expresion();lista_expresiones_repetitiva()
    else:
        logger.info('error de sintaxis: lista_expresiones()') 
        imprimirPosiciones()

def lista_expresiones_repetitiva():
    if preanalisis['v'] ==',':
        m(',');sumar_parametro_actual();expresion();lista_expresiones_repetitiva()

def expresion():
    if en_primeros('expresion_simple'):
        expresion_simple();relacion_opcional()
    else:
        en('expresion()')
        logger.info('error de sintaxis: la expresion no se inicio de manera correcta')
        imprimirPosiciones()

def relacion_opcional():
    if en_primeros('relacion'):
        relacion();expresion_simple()

def relacion():
    # esta es una forma reducida de calcular el primero() y el match para cada elemento
    terminales = ['=','<>','<=','<','>','>=']
    if preanalisis['v'] in terminales:
        m_list(terminales)
    else:
        en('relacion()')
        logger.info("error de sintaxis: se esperaba un operrador relacional, sea '=','<>','<=','<','>' o '>='")
        imprimirPosiciones()

def expresion_simple():
    if en_primeros('mas_menos_opcional') or  en_primeros('termino'):
        mas_menos_opcional();termino();expresion_simple_repetitiva()
    else:
        en('expresion_simple()')
        logger.info('error de sintaxis: se espera un termino valido.')
        imprimirPosiciones()

def mas_menos_opcional():
    terminales = ['+','-']
    if preanalisis['v'] in terminales:
        m_list(terminales)

def expresion_simple_repetitiva():
    global expresion_actual
    if en_primeros('mas_menos_or') or  en_primeros('termino'):
        mas_menos_or();termino();expresion_simple_repetitiva()

def mas_menos_or():
    global expresion_actual
    terminales = ['+','-','or']
    if preanalisis['v'] in terminales:
        if preanalisis['v'] == '+':
            expresion_actual = 'aritmetica'

        m_list(terminales)
    else:
        en('mas_menos_or()')
        logger.info('error de sintaxis: se espera una operacion "+", "-" o "or"')
        imprimirPosiciones()

def termino():
    if en_primeros('factor'):
        factor();termino_repetitiva()
    else:
        en('termino()')
        logger.info('error de sintaxis: se espera un factor valido')
        imprimirPosiciones()

def termino_repetitiva():
    global expresion_actual
    expresion_actual = 'aritmetica'
    if preanalisis['v'] == '*':
        expresion_actual = 'aritmetica'
        m('*');factor();termino_repetitiva()
    elif preanalisis['v'] == '/':
        expresion_actual = 'aritmetica'
        m('/');factor();termino_repetitiva()
    elif preanalisis['v'] == 'and':
        expresion_actual = 'aritmetica'
        m('and');factor();termino_repetitiva()


def factor():
    if en_primeros('identificador'):
        guardar_identificador_a_verificar_a_futuro()
        factor_opcional()
    elif en_primeros('numero'):
        numero()
    elif preanalisis['v'] == '(': 
        m('(');expresion();m(')')
    elif preanalisis['v'] == 'not':
        m('not');factor()
    else:
        en('factor()')
        logger.info('error de sintaxis: se espera un factor valido')
        imprimirPosiciones()

def factor_opcional():
    global identificador_a_verificar_a_futuro
    if en_primeros('llamada_funcion'):
        identificador_sin_definir('funcion')
        guardar_nombre_subprograma_para_contar_parametros(identificador_a_verificar_a_futuro)
        llamada_funcion()
        error_aridad('funcion')

    else:
        identificador_sin_definir('variable')

def llamada_funcion():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()

def numero():
    if preanalisis['v'] == 'enteroDato':
        siguiente_terminal()
    else:
        logger.info('error de sintaxis: numero()')
        imprimirPosiciones()


# MANEJO DE IDENTIFICADORES
def identificador():
    global ultimas_variables_declaradas
    reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
'(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'and' ,
'not']
    if preanalisis['v'] in reservadas:
        en('identificador()')
        logger.info('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
        imprimirPosiciones()
    else:
        siguiente_terminal()

def cargar_identificador(atributo,subatributo=None):
    reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
    '(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'and' ,
    'not']
    if preanalisis['v'] in reservadas:
        en('cargar_identificador()')
        logger.info('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
        imprimirPosiciones()
    else:
        # si no se especifica el subatributo, es porque es el mismo que el atributo
        if subatributo is None:
            subatributo = atributo

        # se asigna scope local o global
        tipoScope = asignar_scope(atributo)
        
        # se evaluan errores de colision de nombres
        colision_nombres(subatributo,tipoScope)

        if atributo == 'variable':
            ultimas_variables_declaradas.append(preanalisis['l'])
        # si el elemento es un parametro, se debe sumar al contador de parametros del subprograma actual.
        if subatributo == 'parametro':
            sumar_parametro_formal()
        # si el elemento es un subprograma, se guarda su nombre y se inicializa su contador de parametros
        elif atributo in ['funcion','procedimiento']:
            guardar_nombre_subprograma_para_contar_parametros()
        
        #se inserta en el TL
        pila_TLs.ver_cima().insertar(nombre=preanalisis['l'], atributo=atributo,subatributo=subatributo, tipo_scope=tipoScope)
        
        # logger.info('pos: '+str(pila_TLs.tamanio())+'--'+str(pila_TLs.recuperar_cima())+'\n') # se imprime la tabla de simbolos al tope de la pila
        siguiente_terminal()

def actualizar_identificador(nombre,nombres_datos,nuevos_valores_datos):
     pila_TLs.ver_cima().modificar_datos(nombre,nombres_datos,nuevos_valores_datos)

def guardar_identificador_a_verificar_a_futuro():
    reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
    '(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'and' ,
    'not']
    if preanalisis['v'] in reservadas:
        en('guardar_identificador_a_verificar_a_futuro()')
        logger.info('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
        imprimirPosiciones()
    else:
        global identificador_a_verificar_a_futuro
        identificador_a_verificar_a_futuro=preanalisis['l']
        siguiente_terminal()


def asignar_scope(atributo):
    '''si el atributo es de tipo variable, se le asigna su respectivo scope'''
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

def guardar_nombre_subprograma_para_contar_parametros(nombre_subprograma = None):
    '''
    Se guarda el nombre del subprograma cuyos parametros seran contados.
    Luego del conteo, se volvera a acceder al elemento en la TL.
    '''
    global subprograma_de_parametros_contados
    global parametros
    if nombre_subprograma is None:
        nombre_subprograma =  preanalisis['l']
    parametros = []
    subprograma_de_parametros_contados = nombre_subprograma

# funcion utilizada para sumar parametros a la lista de parametros actuales.
# requiere que se busquen las variables en la tabla de simbolos para determinar su tipo
def sumar_parametro_actual():
    global parametros
    id = preanalisis['l']
    pila_revertida = reversed(pila_TLs.items)
    tipo_dato = ""
    for ts in pila_revertida:
        ts = ts.tabla
        if id in ts.keys():
            tipo_dato = ts[id]['tipo_dato']
    parametros.append((id, tipo_dato))

# funcion utilizada para sumar parametros a la lista de parametros actuales.
# no requiere que se busquen las variables en la tabla de simbolos para determinar su tipo ya que se realiza en actualizar_parametros_subprograma()
def sumar_parametro_formal():
    '''Suma uno al contador de parametros formales para el subprograma que se esta declarando'''
    global parametros
    parametros.append(preanalisis['l'])

def actualizar_parametros_subprograma():
    global subprograma_de_parametros_contados
    global parametros
    global tipo_parametros
    paresOrdenadosParametros = [(parametro, tipo_parametros) for parametro in parametros]
    pila_TLs.items[-2].modificar_dato(subprograma_de_parametros_contados,'parametros', paresOrdenadosParametros)

# DETECCION DE ERRORES SEMANTICOS
 
def colision_nombres(subatributo,tipoScope):
    l = preanalisis['l']
         
    if l in pila_TLs.recuperar_cima().keys():
        tipoScope1 = '' if tipoScope is None else ' '+tipoScope
        tipoScope2 = ' '+pila_TLs.recuperar_cima()[l]['tipo_scope'] if 'tipo_scope' in pila_TLs.recuperar_cima()[l].keys() else ''

        if (pila_TLs.recuperar_cima()[l]['subatributo'] != subatributo):
            logger.info('error semantico: mismo identificador de',subatributo+tipoScope1,'y',pila_TLs.recuperar_cima()[l]['subatributo']+tipoScope2)
            imprimirPosiciones()
        else:
            logger.info('error semantico: dos ' + subatributo + 's ' + pila_TLs.recuperar_cima()[l]['tipo_scope'] + 'es con el mismo nombre')
            imprimirPosiciones() 

def identificador_sin_definir(atributo):
        global expresion_actual
        id = identificador_a_verificar_a_futuro
        pila_revertida = reversed(pila_TLs.items)
        failed = True

        for ts in pila_revertida:
            ts = ts.tabla
            if id in ts.keys():
                if ts[id]['atributo'] == atributo:
                    failed = False
                else:
                    logger.info('no')
                    break
        if failed:
            texto_error = 'error semantico: identificador de '+atributo+' sin definir'
            if atributo == 'funcion':
                texto_error += ' en expresion ' + expresion_actual
            en('identificador_sin_definir()')
            logger.info(texto_error)
            imprimirPosiciones()
        return failed

def error_aridad(atributo):
    global subprograma_de_parametros_contados
    global parametros
    global tipo_parametros

    id = subprograma_de_parametros_contados
    pila_revertida = reversed(pila_TLs.items)
    failed = False
    if id != "write":  
        for ts in pila_revertida:
            ts = ts.tabla
            if id in ts.keys():
                # se obtienen los parametros formales declarados para el subprograma
                parametros_formales = ts[id]['parametros']
                # contar cada tipo de parametro (int o boolean)
                contador_parametros_formales = Counter([elem[1] for elem in parametros_formales]) 
                # agruparlos en pares ordenados
                cantidad_por_tipo_parametros_formales = [(count, key) for key, count in contador_parametros_formales.items()]
                
                parametros_actuales = [(parametro) for parametro in parametros]
                contador_parametros_actuales = Counter([elem[1] for elem in parametros_actuales]) 
                
                cantidad_por_tipo_parametros_actuales = [(count, key) for key, count in contador_parametros_actuales.items()]
                # se compara las cantidades de ambos tipos de parametros sin importar el orden
                if Counter(cantidad_por_tipo_parametros_formales) != Counter(cantidad_por_tipo_parametros_actuales):
                    failed = True
                break
        if failed:
            descripcion_parametros_actuales = ""
            for index, tipo_parametro in enumerate(cantidad_por_tipo_parametros_actuales):
                descripcion_parametros_actuales += str(tipo_parametro[0]) +  " parametro/s de tipo " + str(tipo_parametro[1])
                if index < len(cantidad_por_tipo_parametros_actuales)-1:
                  descripcion_parametros_actuales += " y "
            if descripcion_parametros_actuales == "":
                descripcion_parametros_actuales = "0 parametros"
            descripcion_parametros_formales = ""
            for index, tipo_parametro in enumerate(cantidad_por_tipo_parametros_formales):
                descripcion_parametros_formales += str(tipo_parametro[0]) + " parametro/s de tipo " +  str(tipo_parametro[1])
                if index < len(cantidad_por_tipo_parametros_formales)-1:
                  descripcion_parametros_formales += " y "
            if descripcion_parametros_formales == "":
                descripcion_parametros_formales = "0"
            logger.info('error semantico: pasaje de '+descripcion_parametros_actuales + ' a '+ atributo +' "'+ id + '". Se esperaba/n ' + descripcion_parametros_formales)
            imprimirPosiciones()
    else:
        if len(parametros) != 1:
            failed = True
            logger.info('error semantico: pasaje de '+descripcion_parametros_actuales + ' a '+ atributo +' "'+ id + '" . Se esperaba 1 parametro')
    return failed

def asignar_tipo_a_variables(tipo):
    global ultimas_variables_declaradas
    for var in ultimas_variables_declaradas:
        if var in pila_TLs.items[-1].tabla.keys():
            pila_TLs.items[-1].tabla[var]['tipo_dato']=tipo
            # logger.info("#########DBG2##########\n"+str(pila_TLs.items[-1].tabla)+"\n#######################")
        else:
            logger.info('error que no deberia ocurrir')
    ultimas_variables_declaradas = []

# AUX
def abrir_archivo(archivo):
    """Abre el archivo y devuelve el objeto del archivo."""
    try:
        f = open(archivo, 'r', encoding='utf-8')
        return f
    except IOError:
        logger.info("Error al abrir el archivo.")
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

# metodos de debug
def en(nombre_func):
    flag = False
    if flag:
        logger.info('en ',nombre_func)


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

        'identificador':['id','TRUE','FALSE'],
        'numero':['enteroDato']
    }

    if len(sys.argv) != 2:
        logger.info("Utilizar: python main.py <ruta_del_fuente_origen>")
        sys.exit(1)
    
    global caracter

    ruta_fuente = sys.argv[1]
    #directorio = '../lexical-analyzer/output.out'
    archivo = abrir_archivo(ruta_fuente)
    siguiente_terminal()
    programa()
    logger.info('analisis sintactico-lexico terminado, programa aceptado.')
   
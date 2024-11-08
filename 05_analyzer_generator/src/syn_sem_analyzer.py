import sys
import copy
from loguru import logger
from collections import Counter

from lex_analyzer import lex_obtener_siguiente_token, lex_obtener_posicion
from code_generator import gen_generar_codigo, gen_iniciar_generador, gen_cantidad_variables_declaradas, gen_nivel_lexico_procedimiento, expresion_a_posfijo, gen_infijo_a_posfijo,gen_generar_codigos_expresion_posfija,gen_get_cont_etq_saltos,gen_get_nivel_lexico_y_posicion
from symbol_table import Tabla_simbolos
from pila import Pila

preanalisis = {'v':'','l':''}
pila_TLs = Pila()
ultimas_variables_declaradas = []           # lista de elementos que se utiliza para asignar el tipo de dato a las ultimas variables declaradas
identificador_a_verificar_a_futuro = ''
expresion_actual = ''                       # si la expresion actual a evaluar es aritmetica, condicional, repetitiva o ninguna (cadena vacia).
pila_expresiones = []
parametros = []                             # cuando se declara/invoca una funcion o procedimiento con parametros, se llevara una lista de los mismos
paresOrdenadosParametros = []
subprograma_de_parametros_contados = ''     # aca se guarda el nombre del subprograma cuyos parametros fueron listados, para acceder al mismo luego de listarlos 
tipo_parametros = ''
expresion_semantica_actual = {
    'elementos' : [],
    'tipo' : None,
    'cantidad_ejecutandose' : 0
}
funcion_actual = {
    'habilitado' : False,
    'identificador': '',
    'declaracion_retorno_encontrada': False,
    'tipo_retorno': ''
}
procedimiento_actual = {
    'habilitado' : False,
    'identificador': '',
}
reservadas = ['PROGRAM' , ';' , '.' ,  'VAR' , ':' , 'INTEGER' , 'BOOLEAN' , ',' , 'PROCEDURE' , 'FUNCTION' , 
    '(' , ')' ,  'BEGIN' , 'END' , ':=' , 'IF' , 'THEN' , 'ELSE' , 'WHILE' , 'DO' , '*' , '/' , 'AND']

def finalizar_analisis(mensaje_error):
    row, col = lex_obtener_posicion()
    logger.success(mensaje_error)
    logger.success("fila:"+str(row)+" columna:"+str(col))
    sys.exit(1)

def m(terminal):
    if(terminal == preanalisis['v']):
        siguiente_terminal()
    else:
        finalizar_analisis("error de sintaxis: se esperaba ["+ terminal +"] y se encontro ["+str(preanalisis['v'])+"]")

def m_list(terminales):
    if(preanalisis['v'] in terminales):
        siguiente_terminal()
    else:
        finalizar_analisis("error de sintaxis: se esperaba ",terminales)

def en_primeros(simbolo):
    for primero in primeros[simbolo]:
        if type(primero) == str and preanalisis['v'] == primero:
            return True
        elif callable(primero) and en_primeros(str(primero.__name__)):
            return True
    return False

def siguiente_terminal():
    global expresion_semantica_actual
    elementos_no_evaluables_en_expresion = ['(', ')', ',', ';']
    # Se realizan verificaciones en caso de que se este evaluando una expresion
    if ((expresion_semantica_actual['cantidad_ejecutandose']>0) and (preanalisis['v'] not in elementos_no_evaluables_en_expresion)):
        verificar_tipo_elemento_en_expresion()
    
    preanalisis['v'] = lex_obtener_siguiente_token(archivo)
    if preanalisis['v'] == None:
        return
    logger.debug(f"{preanalisis['v']:<50}{preanalisis['l']:<20}")
    preanalisis['v'] = preanalisis['v'][preanalisis['v'].find('token'):]
    preanalisis['v'] = eval(preanalisis['v'])

def verificar_tipo_elemento_en_expresion():
    global expresion_semantica_actual
    componentesHibridos = ['=', '<>']
    componentesBooleanos = ['booleanDato', 'AND', 'OR', 'NOT']
    componentesNumericos = ['enteroDato', '>', '<', '>=', '<=', '+', '-', '*', '/'] 
    
    # Se verifica que el siguiente terminal no sea de un tipo incompatible con los componentes anteriores en la expresion
    pila_revertida = reversed(pila_TLs.items)
    expresion_valida = True
    # Si el elemento es un id, se debe chequear su tipo de dato en la tabla de simbolos  
    if preanalisis['v'] == 'id':
        id_value = preanalisis['l']
        for ts in pila_revertida:
            ts = ts.tabla
            if id_value in ts.keys():
                if expresion_semantica_actual['tipo'] is None:
                    if(ts[id_value]['atributo'] == 'procedimiento'):
                        finalizar_analisis("error semantico: se esta queriendo recuperar el tipo de valor de retorno de un procedimiento.")
                    else:
                        expresion_semantica_actual['tipo'] = ts[id_value]['tipo_dato']
                elif expresion_semantica_actual['tipo'] != ts[id_value]['tipo_dato']:
                    expresion_valida = False
                break
        expresion_semantica_actual['elementos'].append(preanalisis['l']) 
    else:
        if expresion_semantica_actual['tipo'] is None:
            if preanalisis['v'] in componentesBooleanos:
                expresion_semantica_actual['tipo'] = 'BOOLEAN'
            elif preanalisis['v'] in componentesNumericos:
                expresion_semantica_actual['tipo'] = 'INTEGER'
            else:
                logger.warning("El id no corresponde a ningun tipo de elemento, esto no deberia suceder." + preanalisis['v'])
        else:
            if preanalisis['v'] in componentesBooleanos and expresion_semantica_actual['tipo'] != 'BOOLEAN':
                expresion_valida = False
            elif preanalisis['v'] in componentesNumericos and expresion_semantica_actual['tipo'] != 'INTEGER':
                expresion_valida = False
            elif preanalisis['v'] not in componentesBooleanos and preanalisis['v'] not in componentesNumericos and preanalisis['v'] not in componentesHibridos:
                logger.warning("La operacion tiene elementos que no corresponden a ningun tipo.")
        expresion_semantica_actual['elementos'].append(preanalisis['v']) 
     
    if (not expresion_valida):
        finalizar_analisis("error semantico: la expresion combina elementos de tipo BOOLEANO e INTEGER.")
        #finalizar_analisis("error semantico: la expresion combina elementos de tipo BOOLEANO e INTEGER. "+str(expresion_semantica_actual['elementos']))
    # logger.error(expresion_semantica_actual)    

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
        or arg0 == 'parentesis'
        or arg0 == 'operadorAritmetico'
        or arg0 == 'operadorRelacional'
        or arg0 == 'operadorRelacionalIndividual'
        ):
        preanalisis['l'] = arg1
        return arg1
    
    if arg0 == 'enteroDato' or arg0 == 'booleanDato':
        preanalisis['l'] = arg1
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
    pila_TLs.ver_cima().insertar(
        nombre='read',
        atributo='procedimiento',
        tipo_scope='global'),

# PROGRAMAS Y BLOQUES
def programa(): # Primera funcion ejecutada
    if preanalisis['v'] == 'PROGRAM':
        gen_generar_codigo("INPP")
        incializar_TL_global()
        m("PROGRAM");cargar_identificador('programa');m(';');bloque();m('.')
    else:
        finalizar_analisis(f"error de sintaxis: se esperaba [program], se encontro [{preanalisis['v']}]")

def bloque():
    global gen_cantidad_variables_declaradas
    if en_primeros('declaraciones_variables_opcional') or en_primeros('declaraciones_subrutinas_opcional') or en_primeros('instruccion_compuesta'):
        declaraciones_variables_opcional();gen_generar_codigo("RMEM",str(gen_cantidad_variables_declaradas));gen_cantidad_variables_declaradas = 0;declaraciones_subrutinas_opcional();instruccion_compuesta()
    else:
        finalizar_analisis('error de sintaxis: no se ha declarado el inicio de la función principal del programa')

def declaraciones_variables_opcional():
    if en_primeros("declaraciones_variables"):
        declaraciones_variables()

def declaraciones_subrutinas_opcional():
    if en_primeros("declaraciones_subrutinas"):
        declaraciones_subrutinas()

# DECLARACIONES
def declaraciones_variables():
    if preanalisis['v'] =='VAR':
        m("VAR");declaracion_variable();m(';');declaraciones_variables_repetitivas()
    else:
        finalizar_analisis("error de sintaxis: se esperaba 'VAR', se encontro '",preanalisis['v'],"'")

def declaraciones_variables_repetitivas():
    if en_primeros('declaracion_variable'): 
         declaracion_variable();m(';');declaraciones_variables_repetitivas()

def declaracion_variable():
    if en_primeros('lista_identificadores'):
        lista_identificadores('variable','variable');m(':');tipo()
    else:
        finalizar_analisis("error de sintaxis: no se definieron las variables")

def tipo(): 
    global ultimas_variables_declaradas
    if preanalisis['v'] == 'INTEGER':
        m('INTEGER')
        sem_asignar_tipo_ultimas_variables('INTEGER')
        return 'INTEGER'
    elif preanalisis['v'] == 'BOOLEAN':
        m('BOOLEAN')
        sem_asignar_tipo_ultimas_variables('BOOLEAN')
        return 'BOOLEAN'
    else:
        finalizar_analisis('error de sintaxis: solo se permite tipo INTEGER o boolean')

def lista_identificadores(atributo,subatributo):
    global gen_cantidad_variables_declaradas
    if en_primeros('identificador'):
        cargar_identificador(atributo,subatributo)
        if (subatributo=='variable'):
            gen_cantidad_variables_declaradas = gen_cantidad_variables_declaradas + 1
        lista_identificadores_repetitiva(atributo,subatributo)
    else:
        finalizar_analisis('error de sintaxis: aca deberia ir un identificador')

def lista_identificadores_repetitiva(atributo,subatributo):
    if preanalisis['v'] == ',':
        m(',')
        cargar_identificador(atributo,subatributo)
        lista_identificadores_repetitiva(atributo,subatributo)

def declaraciones_subrutinas():
    if en_primeros('declaracion_procedimiento'):
        declaracion_procedimiento();m(";");declaraciones_subrutinas()
    elif en_primeros('declaracion_funcion'):
        declaracion_funcion();m(";");declaraciones_subrutinas()

def declaracion_procedimiento():
    global procedimiento_actual, gen_nivel_lexico_procedimiento
    if preanalisis['v'] == 'PROCEDURE':
        m('PROCEDURE')
        l1 = gen_get_cont_etq_saltos()
        gen_generar_codigo('DSVS',"l"+str(l1))
        l2 = gen_get_cont_etq_saltos()
        gen_nivel_lexico_procedimiento = gen_nivel_lexico_procedimiento + 1
        gen_generar_codigo("ENPR",str(gen_nivel_lexico_procedimiento),"l"+str(l2))
        procedimiento_actual['habilitado'] = True
        procedimiento_actual['identificador'] = preanalisis['l']
        cargar_identificador('procedimiento')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();m(';');bloque()#instruccion_compuesta()
        gen_nivel_lexico_procedimiento = gen_nivel_lexico_procedimiento - 1
        gen_generar_codigo('NADA',etiqueta_l = "l"+(str(l1)))
        pila_TLs.desapilar()
        procedimiento_actual['identificador']=''
        procedimiento_actual['habilitado'] = False
    else:
        finalizar_analisis("error de sintaxis: se esperaba 'procedure', se encontro '",preanalisis['v'],"'")

def declaracion_funcion():
    global funcion_actual 
    global expresion_semantica_actual
    if preanalisis['v']=='FUNCTION':
        m('FUNCTION');
        gen_generar_codigo("ENPR",str(gen_nivel_lexico_procedimiento))
        funcion_actual['habilitado'] = True
        funcion_actual['identificador'] = preanalisis['l']
        cargar_identificador('funcion')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();m(':');
        funcion_actual['tipo_retorno']=tipo();
        # Se asigna el tipo de retorno a la funcion en la TS y se resetea la configuracion de la funcion actual
        sem_asignar_tipo_funcion(funcion_actual['tipo_retorno'])
        m(';');bloque();
        # chequear si no se encontro una declaracion de retorno para la funcion
        if funcion_actual['declaracion_retorno_encontrada'] == False:
            finalizar_analisis(f'error semantico: funcion {funcion_actual["tipo_retorno"]} [{funcion_actual["identificador"]}] sin retorno.')
        else:
            funcion_actual['identificador'] = ''
            funcion_actual['declaracion_retorno_encontrada'] = False
            funcion_actual['tipo_retorno'] = ''
            funcion_actual['habilitado'] = False
            pila_TLs.desapilar()
    else:
        finalizar_analisis("error de sintaxis: se esperaba 'function', se encontro '",preanalisis['v'],"'")

def parametros_formales_opcional():
    if en_primeros('parametros_formales'):
        parametros_formales()
    sem_establecer_parametros_subprograma()

def parametros_formales():
    if preanalisis['v'] == '(':
        m('(');seccion_parametros_formales();parametros_formales_repetitiva();m(')')
    else:
        finalizar_analisis("error de sintaxis: se esperaba '(', se encontro '",preanalisis['v'],"'")

def parametros_formales_repetitiva():
    if preanalisis['v'] == ';':
        m(';');seccion_parametros_formales();parametros_formales_repetitiva()

def seccion_parametros_formales():
    global tipo_parametros
    if en_primeros('lista_identificadores'):
        lista_identificadores('variable','parametro')
        m(':')
        tipo_parametros=preanalisis['v']
        sem_actualizar_parametros_subprograma()
        tipo()

# INSTRUCCIONES
def instruccion_compuesta():
    if preanalisis['v'] == 'BEGIN':
        m('BEGIN');instruccion();m(';');instruccion_compuesta_repetitiva();m('END')
    else:
        finalizar_analisis("error de sintaxis: se esperaba 'begin', se encontro '",preanalisis['v'],"'")

def instruccion_compuesta_repetitiva():
    if en_primeros('instruccion'):
        instruccion();m(';');instruccion_compuesta_repetitiva()

def instruccion():
    global expresion_actual
    global funcion_actual
    if en_primeros('identificador'):
        evaluandoRetorno = False
        identificador_izquierda_instruccion = preanalisis['l']
        # Verificar si el identificador del primer elemento de la instruccion coincide con el identificador de la funcion
        if preanalisis['l']==funcion_actual['identificador']:
            funcion_actual['declaracion_retorno_encontrada'] = True
            evaluandoRetorno = True
        sem_registrar_subprograma()
        guardar_identificador_a_verificar_a_futuro()
        instruccion_aux(evaluandoRetorno=evaluandoRetorno, identificador_izquierda_instruccion=identificador_izquierda_instruccion)
    elif en_primeros('instruccion_compuesta'):
        instruccion_compuesta()
    elif en_primeros('instruccion_condicional'):
        expresion_actual = 'condicional'
        instruccion_condicional()
    elif en_primeros('instruccion_repetitiva'):
        expresion_actual = 'repetitiva'
        instruccion_repetitiva()
    else:
        finalizar_analisis('error de sintaxis: no se encontro una instruccion valida')

def instruccion_aux(evaluandoRetorno, identificador_izquierda_instruccion):
    if en_primeros('asignacion'):
        if (not evaluandoRetorno):
            if sem_verificar_identificador_funcion(identificador_izquierda_instruccion):
                finalizar_analisis(f'error semantico: asignacion a funcion fuera del ambito de la misma.')
            else:
                sem_identificador_sin_definir("variable")
        asignacion(evaluandoRetorno, identificador_izquierda_instruccion)

        index, posicion = gen_get_nivel_lexico_y_posicion(identificador_izquierda_instruccion, pila_TLs)
        gen_generar_codigo('ALVL',str(index)+','+str(posicion))
    elif en_primeros('llamada_procedimiento'):
        sem_identificador_sin_definir('procedimiento')
        llamada_procedimiento()
    else:
        finalizar_analisis('error de sintaxis: se esperaba una asignacion o la llamada a un procedimiento')

def asignacion(evaluandoRetorno, identificador_izquierda_instruccion):
    if preanalisis['v'] == ':=':
        if identificador_izquierda_instruccion == procedimiento_actual['identificador']:
            finalizar_analisis(f'error semantico: variable de retorno de funcion usada en procedimiento.')
        m(':=');expresion(evaluandoRetorno)
    else:
        finalizar_analisis("error de sintaxis: se esperaba ':=', se encontro '",preanalisis['v'],"'")
        
def sem_verificar_identificador_funcion(identificador_izquierda_instruccion):
    id = identificador_izquierda_instruccion
    pila_revertida = reversed(pila_TLs.items)
    failed = False

    for ts in pila_revertida:
        ts = ts.tabla
        if id in ts.keys() and ts[id]['atributo'] == "funcion":
            failed = True
            break
    return failed

def llamada_procedimiento():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()
        sem_error_aridad('procedimiento')
    else:
        finalizar_analisis("error de sintaxis: no se cumple la estructura para llamar un procedimiento")

def lista_expresiones_opcional():
    if preanalisis['v'] == '(':
        nombre_proc = identificador_a_verificar_a_futuro
        if nombre_proc == 'read':
            gen_generar_codigo('LEER')

        m('(')
        lista_expresiones_procedimiento();
        m(')')

        if nombre_proc == 'write':
            gen_generar_codigo('IMPR')

def instruccion_condicional():
    if preanalisis['v'] == 'IF':
        m('IF');
        valor_expresion_evaluada = expresion()
        l1 = gen_get_cont_etq_saltos()
        gen_generar_codigo('DSVF',"l"+str(l1))
        if (valor_expresion_evaluada == 'EXPRESION_INTEGER'):
            finalizar_analisis("error semantico: uso de expresion INTEGER como condición de if")
        m('THEN');instruccion();else_opcional(l1)
    else:
        finalizar_analisis("error de sintaxis: se esperaba'if', se encontro ["+preanalisis['v']+"]")

def else_opcional(l1):
    if preanalisis['v'] == 'ELSE':
        m('ELSE');

        l2 = gen_get_cont_etq_saltos()
        gen_generar_codigo('DSVS',"l"+(str(l2)))
        gen_generar_codigo('NADA',etiqueta_l = "l"+(str(l1)))
        instruccion()
        gen_generar_codigo('NADA',etiqueta_l = "l"+(str(l2)))
    else:
        gen_generar_codigo('NADA',etiqueta_l = "l"+(str(l1)))



def instruccion_repetitiva():
    if preanalisis['v'] == 'WHILE':
        m('WHILE')
        l1 = gen_get_cont_etq_saltos()
        gen_generar_codigo('NADA',"l"+(str(l1)))

        valor_expresion_evaluada = expresion()
        l2 = gen_get_cont_etq_saltos()
        gen_generar_codigo('DSVF',"l"+(str(l2)))

        if (valor_expresion_evaluada == 'EXPRESION_INTEGER'):
            finalizar_analisis("error semantico: uso de expresion INTEGER como condición de while")
        m('DO');instruccion()

        gen_generar_codigo('DSVS',"l"+(str(l1)))
        gen_generar_codigo('NADA',"l"+(str(l2)))

    else:
        finalizar_analisis("error de sintaxis:  se esperaba 'while', se encontro ["+preanalisis['v']+"]")

# EXPRESIONES
def lista_expresiones_procedimiento():
    if en_primeros('lista_expresiones'):
        lista_expresiones()

def lista_expresiones():
    global expresion_semantica_actual
    if en_primeros('expresion'):
        if expresion_semantica_actual['cantidad_ejecutandose']>0:
            pila_expresiones.append(copy.copy(expresion_semantica_actual))
            expresion(sumandoParametroActual = True)
            expresion_semantica_actual = pila_expresiones.pop()
        else:
            expresion(sumandoParametroActual = True)
        lista_expresiones_repetitiva()
    else:
        finalizar_analisis('error de sintaxis: lista_expresiones()') 

def lista_expresiones_repetitiva():
    global expresion_semantica_actual
    if preanalisis['v'] ==',':
        m(',');
        if expresion_semantica_actual['cantidad_ejecutandose']>0:
            pila_expresiones.append(copy.copy(expresion_semantica_actual))
            expresion(sumandoParametroActual = True)
            expresion_semantica_actual = pila_expresiones.pop()
        else:
            expresion(sumandoParametroActual = True)
        lista_expresiones_repetitiva()

def expresion(evaluandoRetorno = False, sumandoParametroActual = False):
    global expresion_semantica_actual
    global expresion_a_posfijo
    global funcion_actual, procedimiento_actual
    expresion_semantica_actual['tipo'] = None   
    expresion_semantica_actual['elementos'] = []

    if en_primeros('expresion_simple'):
        # Se inicializa la expresion infija
        expresion_a_posfijo = ''

        # Se comienza a evaluar sintacticamente la expresion actual
        expresion_semantica_actual['cantidad_ejecutandose'] = expresion_semantica_actual['cantidad_ejecutandose'] + 1
        
        expresion_simple()
        es_expresion_comparativa = relacion_opcional()
        if es_expresion_comparativa:  
            tipo_expresion_resultado = "EXPRESION_BOOLEAN"
        else:
            tipo_expresion_resultado = f"EXPRESION_{expresion_semantica_actual['tipo']}"
        if (evaluandoRetorno and funcion_actual['tipo_retorno'] != expresion_semantica_actual['tipo']):
            finalizar_analisis(f"error semantico: el tipo de retorno [{funcion_actual['tipo_retorno']}] y el valor de la expresion [{expresion_semantica_actual['tipo']}] no coinciden.")
        if (sumandoParametroActual):
            sem_sumar_parametro_actual(tipo_expresion_resultado)
        
        # Fin de evaluacion de expresion
        expresion_semantica_actual['cantidad_ejecutandose'] = expresion_semantica_actual['cantidad_ejecutandose'] - 1

        # se convierte la expresion a posfijo
        posfijo = gen_infijo_a_posfijo(expresion_a_posfijo)
        print('POSFIJO: ',posfijo)
        gen_generar_codigos_expresion_posfija(posfijo,pila_TLs)

        return tipo_expresion_resultado
    else:
        finalizar_analisis('error de sintaxis: la expresion no se inicio de manera correcta')

def relacion_opcional():
    if en_primeros('relacion'):
        relacion();expresion_simple()
        return True
    else:
        return False

def relacion():
    # esta es una forma reducida de calcular el primero() y el match para cada elemento
    terminales = ['=','<>','<=','<','>','>=']
    global expresion_a_posfijo

    if preanalisis['v'] in terminales:
        expresion_a_posfijo += ' ' + preanalisis['l']
        m_list(terminales)
    else:
        finalizar_analisis("error de sintaxis: se esperaba un operador relacional, sea '=','<>','<=','<','>' o '>='")

def expresion_simple():
    if en_primeros('mas_menos_opcional') or en_primeros('termino'):
        mas_menos_opcional();termino();expresion_simple_repetitiva()
    else:
        finalizar_analisis('error de sintaxis: se espera un termino valido.')

def mas_menos_opcional():
    terminales = ['+','-']
    global expresion_a_posfijo

    if preanalisis['v'] in terminales:
        expresion_a_posfijo += ' ' + preanalisis['l']
        m_list(terminales)

def expresion_simple_repetitiva():
    if en_primeros('mas_menos_or') or en_primeros('termino'):
        mas_menos_or();termino();expresion_simple_repetitiva()

def mas_menos_or():
    global expresion_actual
    global expresion_a_posfijo
    terminales = ['+','-','OR']

    if preanalisis['v'] in terminales:
        if preanalisis['v'] == '+' or preanalisis['v'] == '-':
            expresion_actual = 'aritmetica'
        elif preanalisis['v'] == 'OR':
            expresion_actual = 'logica'

        expresion_a_posfijo += ' ' + preanalisis['l']
        m_list(terminales)
    else:
        finalizar_analisis('error de sintaxis: se espera una operacion "+", "-" o "OR"')

def termino():
    if en_primeros('factor'):
        factor();termino_repetitiva()
    else:
        finalizar_analisis('error de sintaxis: se espera un factor valido')

def termino_repetitiva():
    global expresion_actual
    global expresion_a_posfijo

    if preanalisis['v'] == '*':
        expresion_actual = 'aritmetica'
        expresion_a_posfijo += ' ' + preanalisis['l']
        m('*');factor();termino_repetitiva()

    elif preanalisis['v'] == '/':
        expresion_actual = 'aritmetica'
        expresion_a_posfijo += ' ' + preanalisis['l']
        m('/');factor();termino_repetitiva()

    elif preanalisis['v'] == 'AND':
        expresion_actual = 'logica'
        expresion_a_posfijo += ' ' + preanalisis['l']
        m('AND');factor();termino_repetitiva()

def factor():
    global expresion_semantica_actual
    global expresion_a_posfijo

    if en_primeros('identificador'):
        guardar_identificador_a_verificar_a_futuro()
        factor_opcional()

    elif en_primeros('numero'):
        numero()

    elif en_primeros('booleano'):
        booleano()

    elif preanalisis['v'] == '(': 
        pila_expresiones.append(copy.copy(expresion_semantica_actual))

        expresion_a_posfijo += ' ' + preanalisis['l']
        m('(')

        valor_expresion_evaluada = expresion()

        expresion_a_posfijo += ' ' + preanalisis['l']
        m(')')

        expresion_semantica_actual = pila_expresiones.pop()
        expresion_semantica_actual['elementos'].append(valor_expresion_evaluada)
        if expresion_semantica_actual['tipo'] is None:
            if valor_expresion_evaluada == "EXPRESION_INTEGER":
                expresion_semantica_actual['tipo'] = "INTEGER"
            elif valor_expresion_evaluada == "EXPRESION_BOOLEAN":
                expresion_semantica_actual['tipo'] = "BOOLEAN"
            else:
                 logger.error("error semantico detectado.")
        elif ((valor_expresion_evaluada == "EXPRESION_INTEGER" and expresion_semantica_actual['tipo'] == "BOOLEAN") or valor_expresion_evaluada == "EXPRESION_BOOLEAN" and expresion_semantica_actual['tipo'] == "INTEGER"):
            finalizar_analisis('error semantico: la expresion combina elementos de tipo BOOLEANO e INTEGER.' + str(expresion_semantica_actual['elementos']))
            
    elif preanalisis['v'] == 'NOT':
        expresion_a_posfijo += ' ' + preanalisis['l']
        m('NOT');factor()

    else:
        # sys._getframe().print_stack()
        finalizar_analisis('error de sintaxis: se espera un factor valido')
        

def factor_opcional():
    global identificador_a_verificar_a_futuro
    if en_primeros('llamada_funcion'):
        sem_identificador_sin_definir('funcion')
        sem_registrar_subprograma(identificador_a_verificar_a_futuro)
        llamada_funcion()
        sem_error_aridad('funcion')
    else:
        sem_identificador_sin_definir('variable')

def llamada_funcion():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()

def numero():
    global expresion_a_posfijo
    if preanalisis['v'] == 'enteroDato':
        expresion_a_posfijo += ' ' + preanalisis['l']
        siguiente_terminal()
    else:
        finalizar_analisis('error de sintaxis: numero()')
        
def booleano():
    global expresion_a_posfijo
    if preanalisis['v'] == 'booleanDato':
        expresion_a_posfijo += ' ' + preanalisis['l']
        siguiente_terminal()
    else:
        finalizar_analisis('error de sintaxis: booleano()')
        
# MANEJO DE IDENTIFICADORES
def identificador():
    global ultimas_variables_declaradas
    global reservadas

    if preanalisis['v'] in reservadas:
        finalizar_analisis('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
    else:
        siguiente_terminal()

def cargar_identificador(atributo,subatributo=None):
    global reservadas
    if preanalisis['v'] in reservadas:
        finalizar_analisis('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
    else:
        # si no se especifica el subatributo, es porque es el mismo que el atributo
        if subatributo is None:
            subatributo = atributo

        # se asigna scope local o global
        tipoScope = sem_asignar_scope(atributo)
        
        # se evaluan errores de colision de nombres
        sem_colision_nombres(subatributo,tipoScope)

        if atributo == 'variable':
            ultimas_variables_declaradas.append(preanalisis['l'])
        # si el elemento es un parametro, se debe sumar al contador de parametros del subprograma actual.
        if subatributo == 'parametro':
            sem_sumar_parametro_formal()
        # si el elemento es un subprograma, se guarda su nombre y se inicializa su contador de parametros
        elif atributo in ['funcion','procedimiento']:
            sem_registrar_subprograma()
        
        # se inserta en el TL
        pila_TLs.ver_cima().insertar(nombre=preanalisis['l'], atributo=atributo,subatributo=subatributo, tipo_scope=tipoScope)
        # finalizar_analisis('pos: '+str(pila_TLs.tamanio())+'--'+str(pila_TLs.recuperar_cima())+'\n') # se imprime la tabla de simbolos al tope de la pila
        siguiente_terminal()

def actualizar_identificador(nombre,nombres_datos,nuevos_valores_datos):
     pila_TLs.ver_cima().modificar_datos(nombre,nombres_datos,nuevos_valores_datos)

def guardar_identificador_a_verificar_a_futuro():
    global reservadas
    global expresion_a_posfijo

    if preanalisis['v'] in reservadas:
        finalizar_analisis('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
    else:
        global identificador_a_verificar_a_futuro
        expresion_a_posfijo += ' ' + preanalisis['l']
        identificador_a_verificar_a_futuro=preanalisis['l']
        siguiente_terminal()


def sem_asignar_scope(atributo):
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

def sem_registrar_subprograma(nombre_subprograma = None):
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
def sem_sumar_parametro_actual(tipo_expresion):
    global expresion_semantica_actual
    global parametros
    if tipo_expresion == "EXPRESION_INTEGER":
        tipo_parametro = "INTEGER"
    elif tipo_expresion == "EXPRESION_BOOLEAN":
        tipo_parametro = "BOOLEAN"
    parametros.append(tipo_parametro)

# funcion utilizada para sumar parametros a la lista de parametros actuales.
# no requiere que se busquen las variables en la tabla de simbolos para determinar su tipo ya que se realiza en sem_actualizar_parametros_subprograma()
def sem_sumar_parametro_formal():
    '''Suma uno al contador de parametros formales para el subprograma que se esta declarando'''
    global parametros
    parametros.append(preanalisis['l'])

def sem_actualizar_parametros_subprograma():
    global subprograma_de_parametros_contados
    global parametros
    global tipo_parametros
    global paresOrdenadosParametros
    paresOrdenadosTemporal = [(parametro, tipo_parametros) for parametro in parametros]
    paresOrdenadosParametros.extend(paresOrdenadosTemporal)
    parametros = []
    
def sem_establecer_parametros_subprograma():
    global subprograma_de_parametros_contados
    global paresOrdenadosParametros
    pila_TLs.items[0].modificar_dato(subprograma_de_parametros_contados,'parametros', paresOrdenadosParametros)
    paresOrdenadosParametros = []

# DETECCION DE ERRORES SEMANTICOS
def sem_colision_nombres(subatributo,tipoScope):
    l = preanalisis['l']
    if l in pila_TLs.recuperar_cima().keys():
        tipoScope1 = '' if tipoScope is None else ' '+tipoScope
        tipoScope2 = ' '+pila_TLs.recuperar_cima()[l]['tipo_scope'] if 'tipo_scope' in pila_TLs.recuperar_cima()[l].keys() else ''
        if (pila_TLs.recuperar_cima()[l]['subatributo'] != subatributo):
            finalizar_analisis('error semantico: mismo identificador de ' + subatributo+tipoScope1 + ' y ' + pila_TLs.recuperar_cima()[l]['subatributo']+tipoScope2 +' ['+l+']')
        else:
            finalizar_analisis('error semantico: dos ' + subatributo + 's ' + pila_TLs.recuperar_cima()[l]['tipo_scope'] + ' con el mismo nombre ['+l+']')
 

def sem_identificador_sin_definir(atributo):
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
                    logger.warning('error semantico que no deberia ocurrir')
                    break
        if failed:
            texto_error = 'error semantico: identificador de '+ atributo +' ['+id+'] sin definir '
            if atributo == 'funcion':
                texto_error += 'en expresion ' + expresion_actual
            finalizar_analisis(texto_error)

        return failed

def sem_error_aridad(atributo):
    global pila_TLs
    global subprograma_de_parametros_contados
    global parametros
    global tipo_parametros

    id = subprograma_de_parametros_contados
    pila_revertida = reversed(pila_TLs.items)
    failed = False
    if id != "write" and id != "read":  
        for ambito in pila_revertida:
            ts = ambito.tabla
            if id in ts.keys():
                # Se obtienen los parametros formales declarados para el subprograma
                parametros_formales = ts[id]['parametros']
                # Contar cada tipo de parametro (int o boolean)
                contador_parametros_formales = Counter([elem[1] for elem in parametros_formales]) 
                # Agruparlos en pares ordenados
                cantidad_por_tipo_parametros_formales = [(count, key) for key, count in contador_parametros_formales.items()]
                
                # Repetir proceso con parametros actuales
                parametros_actuales = [(parametro) for parametro in parametros]
                contador_parametros_actuales = Counter([elem for elem in parametros_actuales]) 
                cantidad_por_tipo_parametros_actuales = [(count, key) for key, count in contador_parametros_actuales.items()]
                
                # Se compara las cantidades de ambos tipos de parametros sin importar el orden
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
            finalizar_analisis('error semantico: pasaje de '+descripcion_parametros_actuales + ' a '+ atributo +' ['+ id + ']. Se esperaba/n ' + descripcion_parametros_formales)
    else:
        # Chequea si el llamado al procedimiento write/read cuenta con exactamente 1 parametro
        if len(parametros) < 1:
            parametros_actuales = [(parametro) for parametro in parametros]
            contador_parametros_actuales = Counter([elem for elem in parametros_actuales]) 
            cantidad_por_tipo_parametros_actuales = [(count, key) for key, count in contador_parametros_actuales.items()]
            descripcion_parametros_actuales = ""
            for index, tipo_parametro in enumerate(cantidad_por_tipo_parametros_actuales):
                descripcion_parametros_actuales += str(tipo_parametro[0]) +  " parametro/s de tipo " + str(tipo_parametro[1])
                if index < len(cantidad_por_tipo_parametros_actuales)-1:
                  descripcion_parametros_actuales += " y "
            if descripcion_parametros_actuales == "":
                descripcion_parametros_actuales = "0 parametros"
            finalizar_analisis('error semantico: pasaje de '+descripcion_parametros_actuales + ' a '+ atributo +' ['+ id + ']. Se esperaba al menos 1 parametro')    
    
def sem_asignar_tipo_ultimas_variables(tipo):
    global ultimas_variables_declaradas
    for var in ultimas_variables_declaradas:
        if var in pila_TLs.items[-1].tabla.keys():
            pila_TLs.items[-1].tabla[var]['tipo_dato']=tipo
        else:
            logger.warning('error que no deberia ocurrir')
    ultimas_variables_declaradas = []

def sem_asignar_tipo_funcion(tipo):
    global funcion_actual
    if funcion_actual['identificador'] in pila_TLs.items[-2].tabla.keys():
        pila_TLs.items[-2].tabla[funcion_actual['identificador']]['tipo_dato']=tipo
    else:
        logger.warning('error que no deberia ocurrir')

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

if __name__ == "__main__":
    global caracter

    primeros = {       
        "programa": ["PROGRAM"],
        "bloque":[declaraciones_variables_opcional,declaraciones_subrutinas_opcional,instruccion_compuesta],
        "declaraciones_variables_opcional": [declaraciones_variables,None],
        "declaraciones_subrutinas_opcional": [declaraciones_subrutinas,None],

        "declaraciones_variables":["VAR"],
        "declaraciones_variables_repetitiva":['VAR',None],
        "declaracion_variable":[lista_identificadores],
        "tipo": ["INTEGER","BOOLEAN"],
        "lista_identificadores":[identificador],
        "lista_identificadores_repetitiva":[",",None],
        "declaraciones_subrutinas":[declaracion_procedimiento,declaracion_funcion,None],
        "declaracion_procedimiento":["PROCEDURE"],
        "declaracion_funcion":["FUNCTION"],
        "parametros_formales_opcional":[parametros_formales,None],
        "parametros_formales":["("],
        "parametros_formales_repetitiva":[";",None],
        "seccion_parametros_formales":[lista_identificadores],

        "instruccion_compuesta":['BEGIN'],
        'instruccion_compuesta_repetitiva':[instruccion,None],
        'instruccion':[identificador,instruccion_compuesta,instruccion_condicional,instruccion_repetitiva],
        'instruccion_aux':[asignacion,llamada_procedimiento],
        'asignacion':[':='],
        'llamada_procedimiento':[lista_expresiones_opcional],
        'lista_expresiones_opcional':['(',None],
        'instruccion_condicional':['IF'],
        'else_opcional':['ELSE',None],
        'instruccion_repetitiva':['WHILE'],

        'lista_expresiones':[expresion],
        'lista_expresiones_repetitiva':[',',None],
        'expresion':[expresion_simple],
        'relacion':['=','<>','<=','<','>','>='],
        'expresion_simple':[mas_menos_opcional,termino],
        'mas_menos_opcional':['+','-',None],
        'expresion_simple_repetitiva':[mas_menos_or,termino,None],
        'mas_menos_or':['+','-','OR',None],
        'termino':[factor],
        'termino_repetitiva':['*','/','AND',None],
        'factor':[identificador,numero,booleano,'(','NOT'],
        'factor_opcional':[llamada_funcion,None],
        'llamada_funcion':[lista_expresiones_opcional],

        'identificador':['id'],
        'numero':['enteroDato'],
        'booleano':['booleanDato']
    }

    if len(sys.argv) < 3:
        logger.error("Utilizar: python main.py <ruta_del_fuente_origen> <ruta_del_codigo_destino> [nivel_logger]")
        sys.exit(1)
    ruta_fuente = sys.argv[1]
    ruta_destino = sys.argv[2]
    logger.remove()
    nivel_logger = "DEBUG"
    if (len(sys.argv) > 3 and sys.argv[3] in ["DEBUG", "INFO", "SUCCESS", "WARNING", "CRITICAL"]):
        nivel_logger = sys.argv[3]
        logger.add(sys.stdout, level=nivel_logger, format="<level>{level: <8}</level> | <level>{message}</level>")
    else:
        logger.add(sys.stdout, level=nivel_logger, format="<level>{level: <8}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
        
    gen_iniciar_generador(ruta_destino)
    archivo = abrir_archivo(ruta_fuente)
    siguiente_terminal()
    # comenzar ejecucion del analizador
    programa()
    logger.success('analisis terminado, programa correcto.')

    #######
    ### $ python syn_sem_analyzer.py ../test_analyzers/files/adri.PAS ../test_generator/out/adri.mepa
    #######
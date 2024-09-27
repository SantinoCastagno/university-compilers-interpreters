import sys
from lexical_analyzer import obtener_siguiente_token, obtener_posicion
from symbol_table import Tabla_simbolos
from pila import Pila
from collections import Counter
from loguru import logger

preanalisis = {'v':'','l':''}
pila_TLs = Pila()
ultimas_variables_declaradas = [] # lista de elementos que se utiliza para asignar el tipo de dato a las ultimas variables declaradas
identificador_a_verificar_a_futuro = ''
expresion_actual = '' # si la expresion actual a evaluar es aritmetica, condicional, repetitiva o ninguna (cadena vacia).
pila_expresiones = []
elementos_expresion_actual = []
parametros = [] # cuando se declara/invoca una funcion o procedimiento con parametros, se llevara una lista de los mismos
subprograma_de_parametros_contados = '' # aca se guarda el nombre del subprograma cuyos parametros fueron listados, para acceder al mismo luego de listarlos 
tipo_parametros = ''
tipo_semantico_ultima_expresion = ''

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
reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
    '(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'AND']

def finalizar_analisis(mensaje_error):
    row, col = obtener_posicion()
    logger.success(mensaje_error)
    logger.success("fila:"+str(row)+" columna:"+str(col))
    sys.exit(1)

def m(terminal):
    if(terminal == preanalisis['v']):
        siguiente_terminal()
    else:
        finalizar_analisis("error de sintaxis: se esperaba ["+ terminal +"] y se encontro ["+preanalisis['v']+"]")

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
    global elementos_expresion_actual
    preanalisis['v'] = obtener_siguiente_token(archivo)
    if preanalisis['v'] == None:
        return
    logger.debug(f"{preanalisis['v']:<50}{preanalisis['l']:<20}")
    preanalisis['v'] = preanalisis['v'][preanalisis['v'].find('token'):]
    preanalisis['v'] = eval(preanalisis['v'])
    # TODO: Este chequeo se esta realizando en varios lugares. Se debe decidir entre dejar aca (lo que parece mas conveniente) y dejar en la definicion de la funcion. El mismo razonamiento se debe hacer al evaluar semanticamente las expresiones.
    if (len(elementos_expresion_actual) > 0):
        if funcion_actual['habilitado'] and funcion_actual['declaracion_retorno_encontrada'] and preanalisis['l'] == funcion_actual['identificador']:
            finalizar_analisis(f'error semantico: variable de retorno {funcion_actual["tipo_retorno"]} ['+funcion_actual['identificador']+'] de funcion usada en expresion')

        elif procedimiento_actual['habilitado'] and preanalisis['l'] == procedimiento_actual['identificador']:
            finalizar_analisis(f'error semantico: variable de retorno usada en procedimiento ['+procedimiento_actual['identificador']+']')

        elementos_expresion_actual.append((preanalisis['v'],preanalisis['l']))
        

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
        ):
        return arg1
    
    if arg0 == 'enteroDato' or arg0 == 'booleanDato':
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

# PROGRAMAS Y BLOQUES
def programa(): # Primera funcion ejecutada
    if preanalisis['v'] == 'program':
        incializar_TL_global()
        m("program");cargar_identificador('programa');m(';');bloque();m('.')
    else:
        finalizar_analisis(f"error de sintaxis: se esperaba [program], se encontro [{preanalisis['v']}]")

def bloque():
    if en_primeros('declaraciones_variables_opcional') or en_primeros('declaraciones_subrutinas_opcional') or en_primeros('instruccion_compuesta'):
        declaraciones_variables_opcional();declaraciones_subrutinas_opcional();instruccion_compuesta()
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
    if preanalisis['v'] =='var':
        m("var");declaracion_variable();m(';');declaraciones_variables_repetitivas()
    else:
        finalizar_analisis("error de sintaxis: se esperaba 'var', se encontro '",preanalisis['v'],"'")

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
    if preanalisis['v'] == 'integer':
        m('integer')
        asignar_tipo_ultimas_variables('integer')
        return 'integer'
    elif preanalisis['v'] == 'boolean':
        m('boolean')
        asignar_tipo_ultimas_variables('boolean')
        return 'boolean'
    else:
        finalizar_analisis('error de sintaxis: solo se permite tipo integer o boolean')

def lista_identificadores(atributo,subatributo):
    if en_primeros('identificador'):
        cargar_identificador(atributo,subatributo);lista_identificadores_repetitiva(atributo,subatributo)
    else:
        finalizar_analisis('error de sintaxis: aca deberia ir un identificador')

def lista_identificadores_repetitiva(atributo,subatributo):
    if preanalisis['v'] == ',':
        m(','),cargar_identificador(atributo,subatributo),lista_identificadores_repetitiva(atributo,subatributo)

def declaraciones_subrutinas():
    if en_primeros('declaracion_procedimiento'):
        declaracion_procedimiento();m(";");declaraciones_subrutinas()
    elif en_primeros('declaracion_funcion'):
        declaracion_funcion();m(";");declaraciones_subrutinas()

def declaracion_procedimiento():
    global procedimiento_actual
    if preanalisis['v'] == 'procedure':
        m('procedure')
        procedimiento_actual['habilitado'] = True
        procedimiento_actual['identificador'] = preanalisis['l']
        cargar_identificador('procedimiento')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();m(';');bloque()#instruccion_compuesta()
        pila_TLs.desapilar()
        procedimiento_actual['identificador']=''
        procedimiento_actual['habilitado'] = False
    else:
        finalizar_analisis("error de sintaxis: se esperaba 'procedure', se encontro '",preanalisis['v'],"'")

def declaracion_funcion():
    global funcion_actual 
    global tipo_semantico_ultima_expresion
    if preanalisis['v']=='function':
        m('function');
        funcion_actual['habilitado'] = True
        funcion_actual['identificador'] = preanalisis['l']
        cargar_identificador('funcion')
        pila_TLs.apilar(Tabla_simbolos())
        parametros_formales_opcional();m(':');funcion_actual['tipo_retorno']=tipo();m(';');bloque();
        # chequear si no se encontro una declaracion de retorno para la funcion
        if funcion_actual['declaracion_retorno_encontrada'] == False:
            finalizar_analisis(f'error semantico: funcion {funcion_actual["tipo_retorno"]} [{funcion_actual["identificador"]}] sin retorno.')

        elif (funcion_actual['tipo_retorno'] != tipo_semantico_ultima_expresion):
            finalizar_analisis(f"error semantico: el tipo de retorno [{funcion_actual['tipo_retorno']}] y el valor de la expresion [{tipo_semantico_ultima_expresion}] no coinciden.")

        else:
            # Se asigna el tipo de retorno a la funcion en la TS y se resetea la configuracion de la funcion actual
            # TODO: asignar el tipo de retorno a la funcion
            asignar_tipo_funcion(funcion_actual['tipo_retorno'])
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
    actualizar_parametros_subprograma()

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
        lista_identificadores('variable','parametro');m(':');tipo_parametros=preanalisis['v'];tipo();

# INSTRUCCIONES
def instruccion_compuesta():
    if preanalisis['v'] == 'begin':
        m('begin');instruccion();m(';');instruccion_compuesta_repetitiva();m('end')
    else:
        finalizar_analisis("error de sintaxis: se esperaba 'begin', se encontro '",preanalisis['v'],"'")

def instruccion_compuesta_repetitiva():
    if en_primeros('instruccion'):
        instruccion();m(';');instruccion_compuesta_repetitiva()

def instruccion():
    global expresion_actual
    global funcion_actual
    if en_primeros('identificador'):
        # Verificar si el identificador del primer elemento de la instruccion coincide con el identificar de la funcion
        if preanalisis['l']==funcion_actual['identificador']:
            # Si coinciden, es porque se esta asignando un valor de retorno
            funcion_actual['declaracion_retorno_encontrada'] = True
        elif preanalisis['l'] == procedimiento_actual['identificador']:
            finalizar_analisis(f'error semantico: variable de retorno de funcion usada en procedimiento')

            
        registrar_subprograma_semanticamente()
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
        finalizar_analisis('error de sintaxis: no se encontro una instruccion valida')

def instruccion_aux():
    if en_primeros('asignacion'):
        asignacion()
    elif en_primeros('llamada_procedimiento'):
        identificador_sin_definir('procedimiento')
        llamada_procedimiento()
    else:
        finalizar_analisis('error de sintaxis: se esperaba una asignacion o la llamada a un procedimiento')

def asignacion():
    if preanalisis['v'] == ':=':
        m(':=');expresion()
    else:
        finalizar_analisis("error de sintaxis: se esperaba ':=', se encontro '",preanalisis['v'],"'")

def llamada_procedimiento():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()
        error_aridad('procedimiento')
    else:
        finalizar_analisis("error de sintaxis: no se cumple la estructura para llamar un procedimiento")

def lista_expresiones_opcional():
    if preanalisis['v'] == '(':
        m('(');lista_expresiones_procedimiento();m(')')

def instruccion_condicional():
    if preanalisis['v'] == 'if':
        m('if');expresion();
        if (chequear_expresion_actual_semanticamente() == 'integer'):
            finalizar_analisis("error semantico: uso de expresion integer como condición de if")

        m('then');instruccion();else_opcional()
    else:
        finalizar_analisis("error de sintaxis: se esperaba'if', se encontro ["+preanalisis['v']+"]")

def else_opcional():
    if preanalisis['v'] == 'else':
        m('else');instruccion()   

def instruccion_repetitiva():
    if preanalisis['v'] == 'while':
        m('while');expresion()
        if (chequear_expresion_actual_semanticamente() == 'integer'):
            finalizar_analisis("error semantico: uso de expresion integer como condición de while")

        m('do');instruccion()
    else:
        finalizar_analisis("error de sintaxis:  se esperaba 'while', se encontro ["+preanalisis['v']+"]")

# EXPRESIONES
def lista_expresiones_procedimiento():
    if en_primeros('lista_expresiones'):
        lista_expresiones()

def lista_expresiones():
    if en_primeros('expresion'):
        expresion();sumar_parametro_actual();lista_expresiones_repetitiva()
    else:
        finalizar_analisis('error de sintaxis: lista_expresiones()') 

def lista_expresiones_repetitiva():
    if preanalisis['v'] ==',':
        m(',');expresion();sumar_parametro_actual();lista_expresiones_repetitiva()

def expresion():
    global elementos_expresion_actual
    global tipo_semantico_ultima_expresion
    tipo_semantico_ultima_expresion = ''
    elementos_expresion_actual = []
    if (len(elementos_expresion_actual) > 0):
        pila_expresiones.append(elementos_expresion_actual)
        elementos_expresion_actual = []
    if funcion_actual['habilitado'] and preanalisis['l'] == funcion_actual['identificador']:
        finalizar_analisis(f'error semantico: variable de retorno de funcion {funcion_actual["tipo_retorno"]} usada en expresion')
    elif procedimiento_actual['habilitado'] and preanalisis['l'] == procedimiento_actual['identificador']:
        finalizar_analisis(f'error semantico: variable de retorno de funcion usada en procedimiento')
    elementos_expresion_actual.append((preanalisis['v'],preanalisis['l']))
    if en_primeros('expresion_simple'):
        expresion_simple();relacion_opcional();
        elementos_expresion_actual.pop()
        tipo_semantico_ultima_expresion = chequear_expresion_actual_semanticamente()
        if (len(pila_expresiones)>0):
            elementos_expresion_actual = pila_expresiones.pop()
    else:
        finalizar_analisis('error de sintaxis: la expresion no se inicio de manera correcta')

def relacion_opcional():
    if en_primeros('relacion'):
        relacion();expresion_simple()

def relacion():
    # esta es una forma reducida de calcular el primero() y el match para cada elemento
    terminales = ['=','<>','<=','<','>','>=']
    if preanalisis['v'] in terminales:
        m_list(terminales)
    else:
        finalizar_analisis("error de sintaxis: se esperaba un operrador relacional, sea '=','<>','<=','<','>' o '>='")

def expresion_simple():
    if en_primeros('mas_menos_opcional') or  en_primeros('termino'):
        mas_menos_opcional();termino();expresion_simple_repetitiva()
    else:
        finalizar_analisis('error de sintaxis: se espera un termino valido.')

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
    terminales = ['+','-','OR']
    if preanalisis['v'] in terminales:
        if preanalisis['v'] == '+' or preanalisis['v'] == 'm':
            expresion_actual = 'aritmetica'
        elif preanalisis['v'] == 'OR':
            expresion_actual = 'logica'
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
    if preanalisis['v'] == '*':
        expresion_actual = 'aritmetica'
        m('*');factor();termino_repetitiva()
    elif preanalisis['v'] == '/':
        expresion_actual = 'aritmetica'
        m('/');factor();termino_repetitiva()
    elif preanalisis['v'] == 'AND':
        expresion_actual = 'logica'
        m('AND');factor();termino_repetitiva()

def factor():
    if en_primeros('identificador'):
        guardar_identificador_a_verificar_a_futuro()
        factor_opcional()
    elif en_primeros('numero'):
        numero()
    elif en_primeros('booleano'):
        booleano()
    elif preanalisis['v'] == '(': 
        m('(');expresion();m(')')
    elif preanalisis['v'] == 'NOT':
        m('NOT');factor()
    else:
        # sys._getframe().print_stack()
        finalizar_analisis('error de sintaxis: se espera un factor valido')
        

def factor_opcional():
    global identificador_a_verificar_a_futuro
    if en_primeros('llamada_funcion'):
        identificador_sin_definir('funcion')
        registrar_subprograma_semanticamente(identificador_a_verificar_a_futuro)
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
        finalizar_analisis('error de sintaxis: numero()')
        
def booleano():
    if preanalisis['v'] == 'booleanDato':
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
            registrar_subprograma_semanticamente()
        
        # se inserta en el TL
        pila_TLs.ver_cima().insertar(nombre=preanalisis['l'], atributo=atributo,subatributo=subatributo, tipo_scope=tipoScope)
        
        # finalizar_analisis('pos: '+str(pila_TLs.tamanio())+'--'+str(pila_TLs.recuperar_cima())+'\n') # se imprime la tabla de simbolos al tope de la pila
        siguiente_terminal()

def actualizar_identificador(nombre,nombres_datos,nuevos_valores_datos):
     pila_TLs.ver_cima().modificar_datos(nombre,nombres_datos,nuevos_valores_datos)

def guardar_identificador_a_verificar_a_futuro():
    global reservadas
    if preanalisis['v'] in reservadas:
        finalizar_analisis('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
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

def registrar_subprograma_semanticamente(nombre_subprograma = None):
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
    parametros.append(tipo_semantico_ultima_expresion)

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
            finalizar_analisis('error semantico: mismo identificador de ' + subatributo+tipoScope1 + ' y ' + pila_TLs.recuperar_cima()[l]['subatributo']+tipoScope2 +' ['+l+']')
        else:
            finalizar_analisis('error semantico: dos ' + subatributo + 's ' + pila_TLs.recuperar_cima()[l]['tipo_scope'] + ' con el mismo nombre ['+l+']')
 

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
                    logger.warning('error semantico que no deberia ocurrir')
                    break
        if failed:
            texto_error = 'error semantico: identificador de '+ atributo +' ['+id+'] sin definir '
            if atributo == 'funcion':
                texto_error += 'en expresion ' + expresion_actual
            finalizar_analisis(texto_error)

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
                contador_parametros_actuales = Counter([elem for elem in parametros_actuales]) 
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
            finalizar_analisis('error semantico: pasaje de '+descripcion_parametros_actuales + ' a '+ atributo +' ['+ id + ']. Se esperaba/n ' + descripcion_parametros_formales)

    else:
        if len(parametros) != 1:
            failed = True
            finalizar_analisis('error semantico: pasaje de '+descripcion_parametros_actuales + ' a '+ atributo +' ['+ id + '] . Se esperaba 1 parametro')


# Toda la expresion tiene que pertenecer al mismo tipo de datos. Es decir, o todo tipo entero o todo tipo boolean
def chequear_expresion_actual_semanticamente():
    global elementos_expresion_actual
    componentesBooleanos = ['booleanDato', '=', '<>', 'AND', 'OR', 'NOT']
    componentesNumericos = ['enteroDato', '>', '<', '>=', '<=', '=', '<>', '+', '-', '*', '/']
    
    pila_revertida = reversed(pila_TLs.items)
    
    tipo_expresion = None
    expresion_valida = True

    # Se compara el tipo de dato de cada valor de la expresion para ver si son equivalentes
    for elemento in elementos_expresion_actual:
        # Si el elemento es un id, se debe chequear su tipo de dato en la tabla de simbolos  
        if elemento[0] == 'id':
            id_value = elemento[1]
            for ts in pila_revertida:
                ts = ts.tabla
                if id_value in ts.keys():
                    if tipo_expresion is None:
                        tipo_expresion = ts[id_value]['tipo_dato']
                    else:
                        if tipo_expresion != ts[id_value]['tipo_dato']:
                            expresion_valida = False
        else:
            if tipo_expresion is None:
                if elemento[0] in componentesBooleanos:
                    tipo_expresion = 'boolean'
                elif elemento[0] in componentesNumericos:
                    tipo_expresion = 'integer'
                else:
                    logger.warning("El id no corresponde a ningun tipo de elemento, esto no deberia suceder." + elemento[0])
            else:
                if elemento[0] in componentesBooleanos and tipo_expresion != 'boolean':
                    expresion_valida = False
                elif elemento[0] in componentesNumericos and tipo_expresion != 'integer':
                    expresion_valida = False
                elif elemento[0] not in componentesBooleanos and elemento[0] not in componentesNumericos:
                    logger.warning("La operacion tiene elementos que no corresponden a ningun tipo.")
    
    if (not expresion_valida):
        # TODO: Profundizar mas en el output
        finalizar_analisis("error semantico: la expresion combina elementos de tipo booleano e integer.")
    logger.debug(f'{elementos_expresion_actual} {tipo_expresion}')
    return tipo_expresion               
    
def asignar_tipo_ultimas_variables(tipo):
    global ultimas_variables_declaradas
    for var in ultimas_variables_declaradas:
        if var in pila_TLs.items[-1].tabla.keys():
            pila_TLs.items[-1].tabla[var]['tipo_dato']=tipo
        else:
            logger.warning('error que no deberia ocurrir')
    ultimas_variables_declaradas = []

def asignar_tipo_funcion(tipo):
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

    if len(sys.argv) < 1:
        logger.error("Utilizar: python main.py <ruta_del_fuente_origen>")
        sys.exit(1)
    ruta_fuente = sys.argv[1]
    logger.remove()
    nivel_logger = "DEBUG"
    if (len(sys.argv) > 2 and sys.argv[2] in ["DEBUG", "INFO", "SUCCESS", "WARNING", "CRITICAL"]):
        nivel_logger = sys.argv[2]
        logger.add(sys.stdout, level=nivel_logger, format="<level>{level: <8}</level> | <level>{message}</level>")
    else:
        logger.add(sys.stdout, level=nivel_logger, format="<level>{level: <8}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
        
    archivo = abrir_archivo(ruta_fuente)
    siguiente_terminal()
    # comenzar ejecucion del analizador
    programa()
    logger.success('analisis terminado, programa correcto.')
    
import inspect
import sys
import os
from lexical_analyzer import obtener_siguiente_token, obtener_posicion

preanalisis = {'v':''}
archivo = ''

def imprimirPosiciones():
    row, col = obtener_posicion()
    print("\t\tfila:"+str(row)+"\tcolumna:"+str(col))
    sys.exit(1)

def m(terminal):
    if(terminal == preanalisis['v']):
        siguiente_terminal()
    else:
        print("error de sintaxis: se esperaba '",terminal,"', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def m_list(terminales):
    if(preanalisis['v'] in terminales):
        siguiente_terminal()
    else:
        print("error de sintaxis: se esperaba ",terminales)
        imprimirPosiciones()


def en_primeros(simbolo):
    #print(simbolo)
    for primero in primeros[simbolo]:
        #print(preanalisis['v'],',',primero,'--',type(primero))
        if type(primero) == str and preanalisis['v'] == primero:
            return True
        elif callable(primero) and en_primeros(str(primero.__name__)):
            return True
    return False

def siguiente_terminal():
    preanalisis['v'] = obtener_siguiente_token(archivo)
    #print('SIGUIENTE LINEA: ',preanalisis['v'])
    if preanalisis['v'] == None:
        return
    preanalisis['v'] = preanalisis['v'][preanalisis['v'].find('token'):]
    preanalisis['v'] = eval(preanalisis['v'])
    #print('SIGUIENTE TERMINAL:',preanalisis['v'],'\n')



def token(arg0,arg1):
    tokens_basicos = {
        'puntoComa':';',
        'coma':',',
        'dosPuntos':':',
        'asignacion':':=',
        'punto':'.'
    }
    if (arg0 == 'keyword'
        or arg0 == 'id'
        or arg0 == 'parentesis'
        or arg0 == 'operadorAritmetico'
        or arg0 == 'operadorRelacional'
        or arg0 == 'booleanDato'
        ):
        return arg1
    if arg0 == 'enteroDato':
        return arg0
    if arg0 in tokens_basicos.keys():
        return tokens_basicos[arg0]
    
# PROGRAMAS Y BLOQUES
def programa(): 
    if preanalisis['v'] == 'program':
        m("program");identificador();m(';');bloque();m('.')
    else:
        print_debug('programa()')
        print("error de sintaxis: se esperaba 'program', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def bloque():
    if en_primeros('declaraciones_variables_opcional') or en_primeros('declaraciones_subrutinas_opcional') or en_primeros('instruccion_compuesta'):
        declaraciones_variables_opcional();declaraciones_subrutinas_opcional();instruccion_compuesta()#;m('.')
    else:
        print_debug('bloque()')
        print('error de sintaxis: no se ha declarado el inicio de la función principal del programa')
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
        print_debug('declaraciones_variables()')
        print("error de sintaxis: se esperaba 'var', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def declaraciones_variables_repetitivas():
    #if preanalisis['v'] == 'var':
    if en_primeros('declaracion_variable'): 
         #m("var");
         declaracion_variable();m(';');declaraciones_variables_repetitivas()

def declaracion_variable():
    if en_primeros('lista_identificadores'):
        lista_identificadores();m(':');tipo()
    else:
        print_debug('declaracion_variable()')
        print("error de sintaxis: no se definieron las variables")
        imprimirPosiciones()

def tipo():
    if preanalisis['v'] == 'integer':
        m('integer')
    elif preanalisis['v'] == 'boolean':
        m('boolean')
    else:
        print_debug('tipo()')
        print('error de sintaxis: solo se permite tipo integer o boolean')
        imprimirPosiciones()

def lista_identificadores():
    if en_primeros('identificador'):
        identificador();lista_identificadores_repetitiva()
    else:
        print_debug('lista_identificadores()')
        print('error de sintaxis: aca deberia ir un identificador')
        imprimirPosiciones()

def lista_identificadores_repetitiva():
    if preanalisis['v'] == ',':
        m(','),identificador(),lista_identificadores_repetitiva()

def declaraciones_subrutinas():
    if en_primeros('declaracion_procedimiento'):
        declaracion_procedimiento();m(";");declaraciones_subrutinas()
    elif en_primeros('declaracion_funcion'):
        declaracion_funcion();m(";");declaraciones_subrutinas()

def declaracion_procedimiento():
    if preanalisis['v'] == 'procedure':
        m('procedure');identificador();parametros_formales_opcional();m(';');bloque()#instruccion_compuesta()
    else:
        print_debug('declaracion_procedimiento()')
        print("error de sintaxis: se esperaba 'procedure', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def declaracion_funcion():
    if preanalisis['v']=='function':
        m('function');identificador();parametros_formales_opcional();m(':');tipo();m(';');bloque()#instruccion_compuesta()
    else:
        print_debug('declaracion_funcion()')
        print("error de sintaxis: se esperaba 'function', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()


def parametros_formales_opcional():
    if en_primeros('parametros_formales'):
        parametros_formales()

def parametros_formales():
    if preanalisis['v'] == '(':
        m('(');seccion_parametros_formales();parametros_formales_repetitiva();m(')')
    else:
        print_debug('parametros_formales()')
        print("error de sintaxis: se esperaba '(', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def parametros_formales_repetitiva():
    if preanalisis['v'] == ';':
        m(';');seccion_parametros_formales();parametros_formales_repetitiva()

def seccion_parametros_formales():
    if en_primeros('lista_identificadores'):
        lista_identificadores();m(':');tipo()

# INSTRUCCIONES
def instruccion_compuesta():
    if preanalisis['v'] == 'begin':
        m('begin');instruccion();m(';');instruccion_compuesta_repetitiva();m('end')
    else:
        print_debug('instruccion_compuesta()')
        print("error de sintaxis: se esperaba 'begin', se encontro '",preanalisis['v'],"'")
        imprimirPosiciones()

def instruccion_compuesta_repetitiva():
    if en_primeros('instruccion'):
        instruccion();m(';');instruccion_compuesta_repetitiva()

def instruccion():
    if en_primeros('identificador'):
        identificador();instruccion_aux()
    elif en_primeros('instruccion_compuesta'):
        instruccion_compuesta()
    elif en_primeros('instruccion_condicional'):
        instruccion_condicional()
    elif en_primeros('instruccion_repetitiva'):
        instruccion_repetitiva()
    else:
        print_debug('instruccion()')
        print('error de sintaxis: no se encontro una instruccion valida')
        imprimirPosiciones()

def instruccion_aux():
    if en_primeros('asignacion'):
        asignacion()
    elif en_primeros('llamada_procedimiento'):
        llamada_procedimiento()
    else:
        print_debug('instruccion_aux()')
        print('error de sintaxis: se esperaba una asignacion o la llamada a un procedimiento')
        imprimirPosiciones()

def asignacion():
    if preanalisis['v'] == ':=':
        m(':=');expresion()
    else:
        print_debug('asignacion()')
        print("error de sintaxis: se esperaba ':=', se encontro '",preanalisis['v'],"'")

def llamada_procedimiento():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()
    else:
        print_debug('llamada_procedimiento()')
        print("error de sintaxis: no se cumple la estructura para llamar un procedimiento")

def lista_expresiones_opcional():
    if preanalisis['v'] == '(':
        m('(');lista_expresiones_procedimiento();m(')')

def instruccion_condicional():
    if preanalisis['v'] == 'if':
        m('if');expresion();m('then');instruccion();else_opcional()
    else:
        print_debug('instruccion_condicional()')
        print("error de sintaxis: se esperaba'if', se encontro '",preanalisis['v'],"'")


def else_opcional():
    if preanalisis['v'] == 'else':
        m('else');instruccion()   

def instruccion_repetitiva():
    if preanalisis['v'] == 'while':
        m('while');expresion();m('do');instruccion()
    else:
        print_debug('error de sintaxis: else_opcional()')
        print("error de sintaxis:  se esperaba 'while', se encontro '",preanalisis['v'],"'")


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
        expresion();lista_expresiones_repetitiva()
    else:
        print('error de sintaxis: lista_expresiones()') 
        imprimirPosiciones()

def lista_expresiones_repetitiva():
    if preanalisis['v'] ==',':
        m(',');expresion();lista_expresiones_repetitiva()

def expresion():
    if en_primeros('expresion_simple'):
        expresion_simple();relacion_opcional()
    else:
        print_debug('expresion()')
        print('error de sintaxis: la expresion no se inicio de manera correcta')
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
        print_debug('relacion()')
        print("error de sintaxis: se esperaba un operrador relacional, sea '=','<>','<=','<','>' o '>='")
        imprimirPosiciones()

def expresion_simple():
    if en_primeros('mas_menos_opcional') or  en_primeros('termino'):
        mas_menos_opcional();termino();expresion_simple_repetitiva()
    else:
        print_debug('expresion_simple()')
        print('error de sintaxis: se espera un termino valido.')
        imprimirPosiciones()


def mas_menos_opcional():
    terminales = ['+','-']
    if preanalisis['v'] in terminales:
        m_list(terminales)

def expresion_simple_repetitiva():
    if en_primeros('mas_menos_or') or  en_primeros('termino'):
        mas_menos_or();termino();expresion_simple_repetitiva()

def mas_menos_or():
    terminales = ['+','-','or']
    if preanalisis['v'] in terminales:
        m_list(terminales)
    else:
        print_debug('mas_menos_or()')
        print('error de sintaxis: se espera una operacion "+", "-" o "or"')
        imprimirPosiciones()

def termino():
    if en_primeros('factor'):
        factor();termino_repetitiva()
    else:
        print_debug('termino()')
        print('error de sintaxis: se espera un factor valido')
        imprimirPosiciones()

def termino_repetitiva():
    if preanalisis['v'] == '*':
        m('*');factor();termino_repetitiva()
    elif preanalisis['v'] == '/':
         m('/');factor();termino_repetitiva()
    elif preanalisis['v'] == 'and':
         m('and');factor();termino_repetitiva()

def factor():
    if en_primeros('identificador'):
       identificador(); factor_opcional()
    elif en_primeros('numero'):
        numero()
    elif preanalisis['v'] == '(': 
        m('(');expresion();m(')')
    elif preanalisis['v'] == 'not':
        m('not');factor()
    else:
        print_debug('factor()')
        print('error de sintaxis: se espera un factor valido')
        imprimirPosiciones()

def factor_opcional():
    if en_primeros('llamada_funcion'):
        llamada_funcion()

def llamada_funcion():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()

# OTROS
def identificador():
    reservadas = ['program' , ';' , '.' ,  'var' , ':' , 'integer' , 'boolean' , ',' , 'procedure' , 'function' , 
'(' , ')' ,  'begin' , 'end' , ':=' , 'if' , 'then' , 'else' , 'while' , 'do' , '*' , '/' , 'and' ,
'not']
    if preanalisis['v'] in reservadas:
        print_debug('identificador()')
        print('error de sintaxis: se esperaba un id, se encontro una palabra reservada: ',preanalisis['v'])
        imprimirPosiciones()
    else:
        siguiente_terminal()

def print_debug(nombre_func):
    activo = False
    if activo:
        print('en ',nombre_func)

def numero():
    if preanalisis['v'] == 'enteroDato':
        siguiente_terminal()
    else:
        print('error de sintaxis: numero()')
        imprimirPosiciones()


# AUX

def abrir_archivo(archivo):
    """Abre el archivo y devuelve el objeto del archivo."""
    try:
        f = open(archivo, 'r', encoding='utf-8')
        return f
    except IOError:
        print("Error al abrir el archivo.")
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
        print("Uso: python main.py <ruta_del_fuente_origen>")
        sys.exit(1)
    
    global caracter

    ruta_fuente = sys.argv[1]
    #directorio = '../lexical-analyzer/output.out'
    archivo = abrir_archivo(ruta_fuente)
    siguiente_terminal()
    programa()
    print('analisis sintactico-lexico terminado, programa aceptado.')
   
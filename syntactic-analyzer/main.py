
preanalisis = {'v':''}

def m(terminal):
    if(terminal == preanalisis['v']):
        siguiente_terminal()
    else:
        print("error de sintaxis: match con ",terminal)

def m_list(terminales):
    if(preanalisis['v'] in terminales):
        siguiente_terminal()
    else:
        print("error de sintaxis: match con ",terminales)


def en_primeros(simbolo):
    #print(simbolo)
    for primero in primeros[simbolo]:
        if simbolo == 'identificador':
            return True
        if type(primero) == str and preanalisis['v'] == primero:
            return True
        elif callable(primero) and en_primeros(str(primero.__name__)):
            return True
    return False

def siguiente_terminal():
    preanalisis['v'] = leer_siguiente_linea(archivo)
    preanalisis['v'] = preanalisis['v'][preanalisis['v'].find('token'):]
    preanalisis['v'] = eval(preanalisis['v'])
    print('SIGUIENTE TERMINAL:',preanalisis['v'])


def token(arg0,arg1):
    tokens_basicos = {
        'puntoComa':';',
        'coma':',',
        'dosPuntos':':',
        'asignacion':':=',
        'suma':'+',
        'resta':'-',
        'div':'/',
        'distinto':'<>',
    }
    if (arg0 == 'keyword'
        or arg0 == 'id'
        or arg0 == 'parentesis'
        ):
        return arg1
    if arg0 == 'enteroDato':
        return arg0
    if arg0 in tokens_basicos.keys():
        return tokens_basicos[arg0]
    
# PROGRAMAS Y BLOQUES
def programa(): 
    if preanalisis['v'] == 'program':
        m("program");identificador();m(';');bloque()
    else:
        print("error de sintaxis: programa()")

def bloque():
    if en_primeros('declaraciones_variables_opcional'):
        declaraciones_variables_opcional();declaraciones_subrutinas_opcional();instruccion_compuesta();m('.')
    else:
        print('error de sintaxis: bloque()')

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
        print('error de sintaxis: declaraciones_variables()')

def declaraciones_variables_repetitivas():
    if preanalisis['v'] == 'var':
         m("var");declaracion_variable();declaraciones_variables_repetitivas()

def declaracion_variable():
    if en_primeros('lista_identificadores'):
        lista_identificadores();m(':');tipo()
    else:
        print('error de sintaxis: declaracion_variable()')

def tipo():
    if preanalisis['v'] == 'integer':
        m('integer')
    elif preanalisis['v'] == 'boolean':
        m('boolean')
    else:
        print('error de sintaxis: tipo()')

def lista_identificadores():
    if en_primeros('identificador'):
        identificador();lista_identificadores_repetitiva()
    else:
        print('error de sintaxis: lista_identificadores()')

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
        m('procedure');identificador();parametros_formales_opcional();m(';');bloque()
    else:
        print('error de sintaxis: declaracion_procedimiento()')

def declaracion_funcion():
    if preanalisis['v']=='function':
        m('function');identificador();parametros_formales_opcional();m(':');tipo();m(';');bloque()
    else:
        print('error de analisis: declaracion_funcion()')

def parametros_formales_opcional():
    if en_primeros('parametros_formales'):
        parametros_formales()

def parametros_formales():
    if preanalisis['v'] == '(':
        m('(');seccion_parametros_formales();parametros_formales_repetitiva();m(')')
    else:
        print('error de sintaxis: parametros_formales()')

def parametros_formales_repetitiva():
    if preanalisis['v'] == ';':
        m(';');seccion_parametros_formales();parametros_formales_repetitiva()

def seccion_parametros_formales():
    if en_primeros('lista_identificadores'):
        lista_identificadores();m(':');tipo()

# INSTRUCCIONES
def instruccion_compuesta():
    if preanalisis['v'] == 'begin':
        m('begin');instruccion();instruccion_compuesta_repetitiva()
    else:
        print('error de sintaxis: instruccion_compuesta()')

def instruccion_compuesta_repetitiva():
    if en_primeros('instruccion'):
        instruccion();m('m');instruccion_compuesta_repetitiva

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
        print('error de sintaxis: instruccion()')

def instruccion_aux():
    if en_primeros('asignacion'):
        asignacion()
    if en_primeros('llamada_procedimiento'):
        llamada_procedimiento()
    else:
        print('error de sintaxis: instruccion_aux()')

def asignacion():
    if preanalisis['v'] == ':=':
        m(':=');expresion()
    else:
        print('error de analisis: asignacion()')

def llamada_procedimiento():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()
    else:
        print('error de analisis: llamada_procedimiento()')

def lista_expresiones_opcional():
    if preanalisis['v'] == '(':
        m('(');lista_expresiones();m(')')

def instruccion_condicional():
    if preanalisis['v'] == 'if':
        m('if');expresion();m('then');instruccion();else_opcional()
    else:
        print('error de sintaxis: instruccion_condicional()')

def else_opcional():
    if preanalisis['v'] == 'else':
        m('else');instruccion()   

def instruccion_repetitiva():
    if preanalisis['v'] == 'while':
        m('while');expresion();m('do');instruccion()
    else:
        print('error de analisis: else_opcional()')

# EXPRESIONES
def lista_expresiones():
    if en_primeros('expresion'):
        expresion();lista_expresiones_repetitiva()
    else:
        print('error de sintaxis: lista_expresiones()') 

def lista_expresiones_repetitiva():
    if preanalisis['v'] ==',':
        m(',');expresion();lista_expresiones_repetitiva()

def expresion():
    if en_primeros('expresion_simple'):
        expresion_simple();relacion_opcional()
    else:
        print('error de sintaxis: expresion()')

def relacion_opcional():
    if en_primeros(relacion):
        relacion();expresion_simple()

def relacion():
    # esta es una forma reducida de calcular el primero() y el match para cada elemento
    terminales = ['=','<>','<=','<','>','>=']
    if preanalisis['v'] in terminales:
        m_list(terminales)
    else:
        print('error de sintaxis: relacion()')

def expresion_simple():
    if en_primeros('mas_menos_opcional'):
        mas_menos_opcional();termino();expresion_simple_repetitiva()

def mas_menos_opcional():
    terminales = ['+','-']
    if preanalisis['v'] in terminales:
        m_list(terminales)

def expresion_simple_repetitiva():
    if en_primeros(mas_menos_or_opcional):
        mas_menos_or_opcional();termino();expresion_simple_repetitiva()

def mas_menos_or_opcional():
    terminales = ['+','-','or']
    if preanalisis['v'] in terminales:
        m_list(terminales)

def termino():
    if en_primeros('factor'):
        factor();termino_repetitiva()
    else:
        print('error de analisis: termino()')

def termino_repetitiva():
    if preanalisis['v'] == '*':
        m('*');factor();termino_repetitiva()
    elif preanalisis['v'] == 'div':
         m('div');factor();termino_repetitiva()
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
        print('error de analisis: factor()')

def factor_opcional():
    if en_primeros('llamada_funcion'):
        llamada_funcion()

def llamada_funcion():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()

# OTROS
def identificador():
    #PREGUNTAR
    siguiente_terminal()

def numero():
    #PREGUNTAR
    siguiente_terminal()


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
        "bloque":[declaraciones_variables_opcional],
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
        'expresion_simple':[mas_menos_opcional],
        'mas_menos_opcional':['+','-',None],
        'expresion_simple_repetitiva':[mas_menos_or_opcional,None],
        'mas_menos_or_opcional':['+','-','or',None],
        'termino':[factor],
        'termino_repetitiva':['*','div','and'],
        'factor':[identificador,numero,'(','not'],
        'factor_opcional':[llamada_funcion,None],
        'llamada_funcion':[lista_expresiones_opcional],

        'identificador':[None]
    }

    directorio = '../lexical-analyzer/output.pas'
    archivo = abrir_archivo(directorio)
    siguiente_terminal()
    programa()


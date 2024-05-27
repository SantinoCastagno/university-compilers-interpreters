

preanalisis = ''
def m(terminal):
    if(terminal == preanalisis):
        preanalisis = siguiente_terminal()
    else:
        print("error de sintaxis")

def m_list(terminales):
    if(preanalisis in terminales):
        preanalisis = siguiente_terminal()
    else:
        print("error de sintaxis")


def en_primeros(simbolo):
    for primero in primeros[simbolo]:
        if type(primero) == str and simbolo == primero:
            return True
        elif type(primero) == function and en_primeros(str(primero)):
            return True
    return False

def siguiente_terminal():
    print()


# PROGRAMAS Y BLOQUES
def programa(): 
    if preanalisis == 'program':
        m("program");identificador();m(';');bloque()
    else:
        print("error de sintaxis")

def bloque():
    if en_primeros('declaraciones_variables_opcional'):
        declaraciones_variables_opcional();declaraciones_subrutinas_opcional();instruccion_compuesta();m('.')
    else:
        print('error de sintaxis')

def declaraciones_variables_opcional():
    if en_primeros("declaraciones_variables"):
        declaraciones_variables()

def declaraciones_subrutinas_opcional():
    if en_primeros("declaraciones_subrutinas"):
        declaraciones_subrutinas()

# DECLARACIONES
def declaraciones_variables():
    if preanalisis =='var':
        m("var");declaracion_variable();declaraciones_variables_repetitivas()
    else:
        print('error de sintaxis')

def declaraciones_variables_repetitivas():
    if preanalisis == 'var':
         m("var");declaracion_variable();declaraciones_variables_repetitivas()

def declaracion_variable():
    if en_primeros('lista_identificadores'):
        lista_identificadores();m(':');tipo()
    else:
        print('error de sintaxis')

def tipo():
    if preanalisis == 'integer':
        m('integer')
    elif preanalisis == 'boolean':
        m('boolean')
    else:
        print('error de sintaxis')

def lista_identificadores():
    if en_primeros('identificador'):
        identificador();lista_identificadores_repetitiva()
    else:
        print('error de sintaxis')

def lista_identificadores_repetitiva():
    if preanalisis == ',':
        m(','),identificador(),lista_identificadores_repetitiva

def declaraciones_subrutinas():
    if en_primeros('declaracion_procedimiento'):
        declaracion_procedimiento();m(";");declaraciones_subrutinas
    elif en_primeros('declaracion_funcion'):
        declaracion_funcion();m(";");declaraciones_subrutinas()

def declaracion_procedimiento():
    if preanalisis == 'procedure':
        m('procedure');identificador();parametros_formales_opcional();m(';');bloque()
    else:
        print('error de sintaxis')

def declaracion_funcion():
    if preanalisis=='function':
        m('function');identificador();parametros_formales_opcional();m(':');tipo();m(';');bloque()
    else:
        print('error de analisis')

def parametros_formales_opcional():
    if en_primeros('parametros_formales'):
        parametros_formales()

def parametros_formales():
    if preanalisis == '(':
        m('(');seccion_parametros_formales();parametros_formales_repetitiva();m(')')
    else:
        print('error de sintaxis')

def parametros_formales_repetitiva():
    if preanalisis == ';':
        m(';');seccion_parametros_formales();parametros_formales_repetitiva()

def seccion_parametros_formales():
    if en_primeros('lista_identificadores'):
        lista_identificadores();m(':');tipo()

# INSTRUCCIONES
def instruccion_compuesta():
    if preanalisis == 'begin':
        m('begin');instruccion();instruccion_compuesta_repetitiva()
    else:
        print('error de sintaxis')

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
        print('error de sintaxis')

def instruccion_aux():
    if en_primeros('asignacion'):
        asignacion()
    if en_primeros('llamada_procedimiento'):
        llamada_procedimiento()
    else:
        print('error de sintaxis')

def asignacion():
    if preanalisis == ':=':
        m(':=');expresion()
    else:
        print('error de analisis')

def llamada_procedimiento():
    if en_primeros('lista_exprexiones_opcional'):
        lista_expresiones_opcional()
    else:
        print('error de analisis')

def lista_expresiones_opcional():
    if preanalisis == '(':
        m('(');lista_expresiones();m(')')

def instruccion_condicional():
    if preanalisis == 'if':
        m('if');expresion();m('then');instruccion();else_opcional()
    else:
        print('error de sintaxis')

def else_opcional():
    if preanalisis == 'else':
        m('else');instruccion()   

def instruccion_repetitiva():
    if preanalisis == 'while':
        m('while');expresion();m('do');instruccion()
    else:
        print('error de analisis')

# EXPRESIONES
def lista_expresiones():
    if en_primeros('expresion'):
        expresion();lista_expresiones_repetitiva()
    else:
        print('error de sintaxis') 

def lista_expresiones_repetitiva():
    if preanalisis ==',':
        m(',');expresion();lista_expresiones_repetitiva()

def expresion():
    if en_primeros('expresion_simple'):
        expresion_simple();relacion_opcional()
    else:
        print('error de sintaxis')

def relacion_opcional():
    if en_primeros(relacion):
        relacion();expresion_simple()

def relacion():
    # esta es una forma reducida de calcular el primero() y el match para cada elemento
    terminales = ['=','<>','<=','<','>','>=']
    if preanalisis in terminales:
        m_list(terminales)
    else:
        print('error de sintaxis')

def expresion_simple():
    if en_primeros('mas_menos_opcional'):
        mas_menos_opcional();termino();expresion_simple_repetitiva()

def mas_menos_opcional():
    terminales = ['+','-']
    if preanalisis in terminales:
        m_list(terminales)

def expresion_simple_repetitiva():
    if en_primeros(mas_menos_or_opcional):
        mas_menos_or_opcional();termino();expresion_simple_repetitiva()

def mas_menos_or_opcional():
    terminales = ['+','-','or']
    if preanalisis in terminales:
        m_list(terminales)

def termino():
    if en_primeros('factor'):
        factor();termino_repetitiva()
    else:
        print('error de analisis: termino()')

def termino_repetitiva():
    #PREGUNTAR santino que pingo es esta aprte de la gramatica
    print()

def factor():
    if en_primeros('identificador'):
        identificador(); factor_opcional()
    elif en_primeros('numero'):
        numero()
    elif preanalisis == '(': #PREGUNTAR aca esta bien?
        m('(');expresion();m(')')
    elif preanalisis == 'not':
        m('not');factor()
    else:
        print('error de analisis: factor()')

def factor_opcional():
    if en_primeros('llamada_funcion'):
        llamada_funcion()

def llamada_funcion():
    if en_primeros('lista_expresiones_opcional'):
        lista_expresiones_opcional()


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
        'termino_repetitiva':[],#PREGUNTAR
        'factor':[identificador,numero,'(','not'],
        'factor_opcional':[llamada_funcion,None],
        'llamada_funcion':[lista_expresiones_opcional]
    }
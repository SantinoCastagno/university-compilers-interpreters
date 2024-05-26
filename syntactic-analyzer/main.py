

preanalisis = ''
def m(terminal):
    if(terminal == preanalisis):
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
        m('procedure');identificador();parametro_formales_opcional();m(';');bloque()
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

def asingacion():
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
        m('while');exprecion();m('do');instruccion()
    else:
        print('error de analisis')

# EXPRESIONES 

if __name__ == "__main__":
    primeros = {
        "programa": ["program"],
        "bloque":[declaraciones_variables_opcional],
        "declaraciones_variables_opcional": [declaraciones_variables,None],
        "declaraciones_subrutinas_opcional": [declaraciones_subrutinas,None],

        "declaraciones_variables":["var"],
        "declaraciones_variables_repetitiva":[lista_identificadores],
        "tipo": ["integer","boolean"],
        "lista_identificadores":[identificador],
        "lista_identificadores_repetitiva":[","],
        "declaraciones_subrutinas":[declaracion_procedimiento,declaracion_funcion,None],
        "declaracion_procedimiento":["procedure"],
        "declaracion_funcion":["function"],
        "parametros_formales_opcional":[parametros_formales,None],
        "parametros_formales":["("],
        "parametros_formales_repetitiva":[";"],
        "seccion_parametrod_formales":[lista_identificadores],
    }
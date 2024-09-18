from typing import Union

class Tabla_simbolos():
    def __init__(self):
        self.tabla = {}

    def insertar(self,nombre,atributo,subatributo=None,tipo_dato=None, parametros=[],tipo_retorno=None,tipo_scope=None):
        self.tabla[nombre] = {'atributo':atributo}
        if subatributo is not None:
            self.tabla[nombre]['subatributo'] = subatributo
        if tipo_dato is not None:
            self.tabla[nombre]['tipo_dato'] = tipo_dato
        if  parametros is not None:
            self.tabla[nombre]['parametros'] = parametros
        if tipo_retorno is not None:
            self.tabla[nombre]['tipo_retorno'] = tipo_retorno
        if tipo_scope is not None:
            self.tabla[nombre]['tipo_scope'] = tipo_scope
    
    def buscar(self,nombre):
        return self.tabla[nombre]
    
    def agregar_parametro(self,nombre,parametro):
        self.tabla[nombre]['parametros'].append(parametro)
    
    def modificar_dato(self,nombre_atributo,nombres_datos,nuevos_valores_datos:Union[str,list]):
        if type(nombres_datos) == str:
            self.tabla[nombre_atributo][nombres_datos] =  nuevos_valores_datos
        elif type(nombres_datos) == list:
            for n_d,n_v_d in zip(nombres_datos,nuevos_valores_datos):
                self.tabla[nombre_atributo][n_d] = n_v_d

    def eliminar(self,nombre):
        del self.tabla[nombre]

from typing import Union

class Tabla_simbolos():
    def __init__(self):
        self.tabla = {}

    def insertar(self,nombre,atributo,subatributo=None,tipo_dato=None,n_parametros=None,
                 tipo_parametros=None,tipo_retorno=None,tipo_scope=None):
        self.tabla[nombre] = {'atributo':atributo}

        if subatributo is not None:
            self.tabla[nombre]['subatributo'] = subatributo

        if tipo_dato is not None:
            self.tabla[nombre]['tipo_dato'] = tipo_dato
        if n_parametros is not None:
            self.tabla[nombre]['n_parametros'] = n_parametros
        if tipo_parametros is not None:
            self.tabla[nombre]['tipo_parametros'] = tipo_parametros
        if tipo_retorno is not None:
            self.tabla[nombre]['tipo_retorno'] = tipo_retorno
        if tipo_scope is not None:
            self.tabla[nombre]['tipo_scope'] = tipo_scope
        # print(self.tabla[nombre])
    
    def buscar(self,nombre):
        return self.tabla[nombre]
    
    def modificar_dato(self,nombre_atributo,nombres_datos,nuevos_valores_datos:Union[str,list]):
        if type(nombres_datos) == str:
            self.tabla[nombre_atributo][nombres_datos] =  nuevos_valores_datos
        elif type(nombres_datos) == list:
            for n_d,n_v_d in zip(nombres_datos,nuevos_valores_datos):
                self.tabla[nombre_atributo][n_d] = n_v_d

    def eliminar(self,nombre):
        del self.tabla[nombre]

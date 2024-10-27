from loguru import logger

ruta_destino = None
gen_cantidad_variables_declaradas = 0 # cantidad de las variables declaradas del programa/subprograma actual, utilizada para reservar el espacio de memoria

def _gen_abrir_archivo():
    global ruta_destino
    try:
        with open(ruta_destino, 'w', encoding='utf-8') as archivo:
            archivo.write("")
    except Exception as e:
        logger.error(f"Ocurrió un error al crear el archivo: {e}")

def gen_generar_codigo(contenido_1, contenido_2 = ""):
    global ruta_destino
    try:
        with open(ruta_destino, 'a', encoding='utf-8') as archivo:
            archivo.write(f"{contenido_1}\t{contenido_2}\n")
    except Exception as e:
        logger.error(f"Ocurrió un error al escribir el archivo: {e}")

def gen_iniciar_generador(ruta):
    global ruta_destino
    ruta_destino = ruta
    _gen_abrir_archivo()
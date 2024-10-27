from loguru import logger

ruta_destino = None

def gen_generar_codigo(contenido):
    global ruta_destino
    try:
        with open(ruta_destino, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
    except Exception as e:
        logger.error(f"Ocurrió un error al escribir el archivo: {e}")

def gen_iniciar_generador(ruta):
    global ruta_destino
    ruta_destino = ruta
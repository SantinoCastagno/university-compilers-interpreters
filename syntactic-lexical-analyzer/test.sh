#!/bin/bash

DIRECTORIO="./pruebas"

if [ ! -d "$DIRECTORIO" ]; then
    echo "El directorio $DIRECTORIO no existe."
    exit 1
fi

for ARCHIVO in "$DIRECTORIO"/*; do
    if [ -f "$ARCHIVO" ]; then
        echo "############################################################" >> ./log.txt
        echo "Analizando sintacticamente el fuente: $ARCHIVO" >> ./log.txt
        python3 syntactic_analyzer.py $ARCHIVO >> ./log.txt
    fi
done

echo "Pruebas completadas sobre todos los archivos fuentes."

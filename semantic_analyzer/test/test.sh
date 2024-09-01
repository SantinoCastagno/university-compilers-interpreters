#!/bin/bash

DIRECTORIO="./files"

if [ ! -d "$DIRECTORIO" ]; then
    echo "El directorio $DIRECTORIO no existe."
    exit 1
fi

rm ./log.txt

for ARCHIVO in "$DIRECTORIO"/*; do
    if [ -f "$ARCHIVO" ]; then
        echo "############################################################" >> ./log.txt
        echo "Analizando sintacticamente el fuente: $ARCHIVO" >> ./log.txt
        python3 ../src/syntactic_analyzer.py $ARCHIVO >> ./log.txt
    fi
done

echo "Pruebas completadas sobre todos los archivos fuentes."

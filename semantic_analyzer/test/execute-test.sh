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
        echo "Analizando $ARCHIVO" >> ./log.txt
        echo "" >> ./log.txt
        python3 ../src/syntactic_analyzer.py $ARCHIVO SUCCESS>> ./log.txt
    fi
done
echo "############################################################" >> ./log.txt
echo "Pruebas completadas sobre todos los archivos fuentes."

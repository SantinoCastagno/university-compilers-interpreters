#!/bin/bash

DIRECTORIO="./test/files"

if [ ! -d "$DIRECTORIO" ]; then
    echo "El directorio $DIRECTORIO no existe."
    exit 1
fi

rm ./test/log.txt

for ARCHIVO in "$DIRECTORIO"/*; do
    if [ -f "$ARCHIVO" ]; then
        echo "############################################################" >> ./test/log.txt
        echo "Analizando $ARCHIVO" >> ./test/log.txt
        echo "" >> ./test/log.txt
        python3 ./src/syntactic_analyzer.py $ARCHIVO SUCCESS>> ./test/log.txt
    fi
done
echo "############################################################" >> ./test/log.txt
echo "Pruebas completadas sobre todos los archivos fuentes."

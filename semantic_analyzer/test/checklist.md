# Checklist de los errores que debemos encontrar

## (a) Colisión de nombres:

- [x] 01A1 - Mismo identificador programa y variable global.
- [x] 01A2 - Mismo identificador programa y procedimiento.
- [x] 01A3 - Mismo identificador programa y función.
- [x] 01B1 - Dos variables globales con el mismo nombre.
- [x] 01B2 - Dos variables locales con el mismo nombre.
- [x] 01C - Mismo identificador variable global y función. 
- [x] 01D - Mismo identificador variable global y procedimiento.
- [x] 01E - Mismo identificador variable local y función local.
- [x] 01F - Mismo identificador variable local y parámetro.
- [x] 01G - Mismo identificador parámetro y función local.

## (b) Identificadores no definidos:

- [x] 02A1 - Identificador de procedimiento sin definir.
- [x] 02A2 - Uso en entorno local de identificador de variable no definido. (parcialmente bien)
- [x] 02A3 - Uso de identificador de función no definido en expresión aritmética. 
- [x] 02A4 - Uso de identificador de función booleana no definido en condición de if.
- [x] 02A5 - Uso de identificador de función booleana no definido en condición de while.

## (c) Aridad no coincidente (Arity mismatch):

- [x] 03A - Pasaje de parámetro a una función sin parámetros.
- [x] 03A1 - Pasaje de un parámetro booleano a función con dos parámetros booleanos.
- [x] 03A2 - Pasaje de tres parámetros booleanos a función con dos parámetros booleanos. 
  - Se agregaron los literales booleanos y ahora son factores validos.
- [x] 03B1 - Pasaje de dos parámetros numéricos a procedimiento con tres parámetros numéricos.
- [x] 03B2 - Pasaje de cuatro parámetros numéricos a procedimiento con tres parámetros numéricos.

## (d) Tipo no coincidente (Type mismatches)

- [x] 03C1 - Pasaje de parámetros booleano y numérico a función con dos parámetros booleanos.
- [x] 03C2 - Pasaje de parámetros numérico y booleano a función con dos parámetros booleanos.
- [x] 03C3 - Pasaje de parámetros numérico y booleano a procedimiento con dos parámetros numéricos.
- [x] 03D1 - Pasaje de parámetros expresión booleana y expresion numérica a función con dos parámetros booleanos.
  - Falta aclarar que es de expresiones y no de variables simples (probablemente no es necesario).
- [x] 03D2 - Pasaje de parámetros expresión booleana y booleano a función con dos parámetros booleanos.
  - Falta aclarar que es de expresiones y no de variables simples (probablemente no es necesario).
  - Fix: Pasaje de parámetros expresión numerica y booleano a procedimiento con dos parámetros númericos.
- [x] 03E1 - Pasaje de parámetros expresión numérica y variable numérica a función con dos parámetros numéricos.
  - El programa es correcto.
- [x] 03E2 - Pasaje de parámetros expresión numérica y constante literal numérica a función con dos parámetros numéricos.
  - El programa es correcto.
- [x] 04A1 - Uso de expresión booleana asignada como retorno de función numérica.
- [x] 04A2 - Uso de expresión numérica asignada como retorno de función booleana.
  - fix: la expresion combina elementos de tipo booleano y numerico
- [x] 04A3 - Uso de operador booleano y variable booleana en expresión numérica asignada como retorno de función numérica.
  - fix: la expresion combina elementos de tipo booleano y numerico
- [x] 04B - Uso de operador y variables boolenadas y numéricas. (OK)
- [x] 04B1 - Uso de operador booleano con expresión de variables numéricas.
- [x] 04B2 - Uso de operador booleano con expresión de variables numéricas.
- [x] 04B3 - Uso de operador numérico con expresión de variables booleanas.
- [x] 04B4 - Uso de operador numérico con expresión de variables booleanas.
- [x] 04B5 - Uso de operadores numérico y booleano con expresión de variables booleanas.
- [ ] 04C1 - Uso de variable numérica como condición de if.
- [ ] 04C2 - Uso de función numérica como condición de if.
- [ ] 04C3 - Uso de expresión numérica como condición de if.
- [ ] 04C4 - Uso de expresión booleana mal formada como condición de if.
- [ ] 04C5 - Uso de expresión booleana bien formada como condición de if. (OK)
- [ ] 04D1 - Uso de expresión booleana mal formada como condición de while.
- [ ] 04D2 - Uso de expresión numérica como condición de while.
- [ ] 04D3 - Uso de variable numérica como condición de while.
- [ ] 04D4 - Uso de constante literal numérica como condición de while.

## (e) Problemas de subrutinas

- [x] 05A1 - Función booleana sin retorno.
- [x] 05A2 - Función numérica sin retorno.
- [x] 05B1 - Variable de retorno de función booleana usada en expresión.
- [x] 05B2 - Variable de retorno de función numérica usada en expresión.
- [x] 05C1 - Variable de retorno de función usada en procedimiento.
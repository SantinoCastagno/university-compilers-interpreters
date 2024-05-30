program OperacionesBasicas;

var
  numero1, numero2, suma, resta, multiplicacion, division: integer;

begin
  { Solicitar al usuario ingresar dos números }
  writeln('Ingrese el primer numero:');
  readln(numero1);
  writeln('Ingrese el segundo numero:');
  readln(numero2);
  
  { Realizar operaciones basicas }
  suma := numero1 + numero2;
  resta := numero1 - numero2;
  multiplicacion := numero1 * numero2;
  
  { Verificar division por cero }
  if numero2 <> 0 then
    division := numero1 / numero2
  else
    writeln('Error: No se puede dividir por cero');
  
  { Mostrar resultados }
  writeln('Suma:');
  writeln(suma);
  writeln('Resta:');
  writeln(resta);
  writeln('Multiplicacion:');
  writeln(multiplicacion);
  if numero2 <> 0 then
    writeln('Division:');
    writeln(division);
    
  readln();   
end.

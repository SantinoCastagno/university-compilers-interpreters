program OperacionesBasicas;

var
  numero1, numero2, suma, resta, multiplicacion, division: real;

begin
  { Solicitar al usuario ingresar dos números }
  writeln('Ingrese el primer número:');
  readln(numero1);
  writeln('Ingrese el segundo número:');
  readln(numero2);
  
  { Realizar operaciones básicas }
  suma := numero1 + numero2;
  resta := numero1 - numero2;
  multiplicacion := numero1 * numero2;
  
  { Verificar división por cero }
  if numero2 <> 0 then
    division := numero1 / numero2
  else
    writeln('Error: No se puede dividir por cero');
  
  { Mostrar resultados }
  writeln('Suma:', suma:0:2);
  writeln('Resta:', resta:0:2);
  writeln('Multiplicación:', multiplicacion:0:2);
  if numero2 <> 0 then
    writeln('División:', division:0:2);
    
  readln; { Esperar a que el usuario presione Enter para salir }
end.

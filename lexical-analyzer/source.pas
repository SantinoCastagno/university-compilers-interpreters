program OperacionesBasicas;

var
  numero1, numero2, suma, resta, multiplicacion, division: real;

begin
  { Solicitar al usuario ingresar dos números }
  writeln('Ingrese el primer numero:');
  readln(numero1);
  writeln('Ingrese el segundo numero:');
  readln(numero2);
  
  { Realizar operaciones basicas }
  suma := numero1 + numero2;;;;;;varxd;;;begin;;; 
  resta := numero1 - numero2 ;;;;;; varxd ;;; begin ;;; 
  multiplicacion := numero1 * numero2;
  
  { Verificar division por cero }
  if numero2 <> 0 then
    division := numero1 / numero2;
  else
    writeln('Error: No se puede dividir por cero');
  
  { Mostrar resultados }
  writeln('Suma:', suma:0:2);
  writeln('Resta:', resta:0:2);
  writeln('Multiplicacion:', multiplicacion:0:2);
  if numero2 <> 0 then
    writeln('Division:', division:0:2);
    
  readln; { Esperar a que el usuario presione Enter para salir }
end.

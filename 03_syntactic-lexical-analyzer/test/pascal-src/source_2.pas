program source1;

var
  numero1, numero2, suma, resta, multiplicacion, division: integer;
 relacion1,relacion2,relacion3: boolean;

procedure miproc1(minum,otronum:integer;mibool,otrobool,ultimobool:boolean);
begin
   readln();
   relacion1 := (-3 > 4) and 1000 + 2 - 4 = suma or 3 <> 3;
   relacion2 := relacion1;
   while relacion2 <> relacion1 do
   suma := -5;

end;



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
    begin
    writeln('Division:');
    writeln(division);
    end    
  else
      writeln('Recuerda, no hubo division!');

  readln();   
end.

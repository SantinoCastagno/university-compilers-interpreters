program prueba ;{ Archivo Prueba C&I Semantico}
var
   a, b: integer;

procedure nuevo (a: integer);
 var j:integer;
begin
  j := a;
  write ( a + j );
end;

begin
  a:=9; {+ algo(a); lo comente porque sino detecta este y rompe}
  while NOT( salida(a) )
    nuevo(a-2);
end.


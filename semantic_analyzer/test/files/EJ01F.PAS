program prueba ;{ Archivo Prueba C&I Semantico}
var
   a, b: integer;

function algo: integer;
 var b:boolean;
begin
  algo := a + 5;
end;

procedure nuevo (a: integer);
 var a:integer;

begin
  write ( a );
end;

begin
  a:=9;
  algo(a*2);
end.


program prueba ;{ Archivo Prueba C&I Semántico}
var
  a, b: integer;
  j,l:boolean;

function algo(m,n:boolean): integer;
 var b:integer;
begin
  if algo(m,n and TRUE)
    then b := +1
    else b := -5;
  algo := a + 5;
end;

procedure nuevo (b,c: integer);
begin
  b := b + c;
  write ( b + a );
end;

begin
   a:= 9 + algo(j, l);
   nuevo(a*2, b);
end.


Program ConductorDePrueba;
Var
  a: integer;
  local: boolean;

function pru(r:integer):integer;
var local: boolean;
begin
  if (r= 0) then pru:= 1
  else
     local:= r-1>2;
end;

Function factorial(r:integer):integer;
var local: integer;
begin
  a:= local;   
  a:= pru(a);

  if r = 1 then
    factorial := 1
  else
    factorial := r * factorial(r-1);
end;

Begin
  a:= local;
  pru:= 33;
  a := factorial(3);
  write(a);
End.

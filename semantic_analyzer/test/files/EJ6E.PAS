Program ConductorDePrueba;
Var a: integer;
    local: integer;

function pru(r:integer):integer;
var local: boolean;
begin
  if (r= 0) then pru:= 1
  else
     local:= r-1>2; 
 

    a:= pru(a);

end;

Function factorial(r:integer):integer;
begin
   
  a:= pru(a);

  if r = 1 then
    factorial := 1
  else
    factorial := r * factorial(r-1);
end;

Begin

  a:= pru(a);


  a:= local;
  pru:= 33;
  local:= pru(33);
  a := factorial(3);
  write(a);
End.

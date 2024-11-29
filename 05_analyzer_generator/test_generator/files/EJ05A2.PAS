program prueba ;{ Archivo Prueba C&I Semántico}
var
  a, b: integer;
  j,l:boolean;

function algo(m,n:boolean): integer;
  var b:integer;
 begin
   if m then b := a + 5 
        else b := a - 5;
   algo := b;
 end;
 
function algoBool(m,n:boolean): boolean;
 var b:boolean;
begin
  b := a - 5 > 3;
  if b  then 
  begin
    if m then algoBool := True else algoBool := False;
  end
  else
  begin
    if n then algoBool := False else algoBool := True;
  end;
end;

procedure nuevo (b,c: integer);
begin
  write( a + b + c );
end;

begin
    read(a);
    read(b);
    write(10);
    j := TRUE;
    write(60);
    l := TRUE;
    write(10);

    if algoBool(j,l) then
    begin  
      a:= 9 + algo(j AND TRUE, l);
      write(a);
    end
    else
      nuevo(a*2, b);
end.


program X;
var AA,G: integer;
    ab: boolean;

function f(a: integer) : integer;
begin
  if a=0 then
    begin
    f:= 1;
    end
  else
    begin
       f:= a*f(a-1);
    end;
  G:= G+1;	
end;

function f1(a: integer) : integer;
begin
   f1:= a * 2;
end;


begin
  G:= 0;
  read(AA);
  write(f(AA));
  write(G);
  write(AA);
  write(f1(AA));
end.

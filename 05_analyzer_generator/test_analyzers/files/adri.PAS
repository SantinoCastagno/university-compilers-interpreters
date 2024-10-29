program b;
var a:integer; 
    t:integer;
    a1: boolean;
    d:boolean; 

procedure XX1;
var a:boolean; 
    d,aver:integer; 

begin
  if 55>3 then
     d:= 55+t+1;
 
  aver:= 33;
  XX1();   {---------> Esta llamada tira error.}

end;

procedure XX2(b2: integer; b1:boolean);
var a:boolean; 
d:integer;

begin
  if 1=2 then
     {d:= 55+t+1;}
     d := 2+1;
     d := 43 * 23 / 2 - 5 * 23-2 >= 13 / 4 / 3 + 2 * 5 - 34 +2 /3;
     {d := 43 * (23 / 2) - 5 * 23-2 >= 13 / 4 / 3 + 2 * 5 - 34 +2 /3;}

  XX1();  {---------> Esta llamada tira error.}
end;


function FF(w:integer): integer;
begin
   FF:= FF(77) + 77;
end;


begin
  a:= 88;
end.

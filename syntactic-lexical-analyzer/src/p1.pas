program prueba;
var
  a,b:integer;
  c:boolean;     

function f (): integer ;
var
  a,b:integer;    { no permite declaraciones aca , en la gramatica esta bien, en la implementacion falla (debe ir bloque y no instruccion compuesta , esta comentado}

begin
   b();
end ;


procedure p (a:integer; b:boolean) ;
var
  a,b:integer;     { no permite declaraciones aca , en la gramatica esta bien, en la implementacion falla (debe ir bloque y no instruccion compuesta , esta comentado}

begin
   b();
end ;


 begin
   a:=9;
   if a <2 and (e<3+r) then      
     if  b=4 then
        c(a,f) 
	else 
      a:=a() ;

   while e do
      if  b=4 then
        c() 
	else 
      a() ;


 end.

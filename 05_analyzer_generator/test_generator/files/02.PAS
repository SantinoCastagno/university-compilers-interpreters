Program ejemplo;
var m,n: integer;

function f(n:integer; k:integer) : integer;
    var p,q:integer;
    begin
        if n<2
            then 
            begin 
                f:=n;
                p:=0;
                end
            else 
            begin
                f:= f(n-1,p)+f(n-2,q);
                p:= p+q+1;
            end;
        write(n);
    end;
    begin
        n := f(3,m);
        write(n);
    end.

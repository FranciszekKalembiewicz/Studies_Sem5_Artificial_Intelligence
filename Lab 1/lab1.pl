%Zadanie1
pierwiastek(X) :- Wynik is sqrt(X), write(Wynik).
pierwiastek_liczba(X) :- Wynik is X**0.5, write(Wynik).

%Zadanie2
logarytm_naturalny(X) :- Wynik is log(X), write(Wynik).

%Zadanie3
miejsce_zerowe(A,B) :- Wynik is -B/A, write(Wynik).

%Zadanie4
miejsce_zerowe_kwadratowe(A,B,C) :- 
Delta is B**2-4*A*C,
(
Delta>0 -> 
X1 is (-B-sqrt(Delta))/(2*A), 
X2 is (-B+sqrt(Delta))/(2*A),
write('Pierwiastki to: '), write(X1), write(' i '), write(X2), nl;
Delta =:= 0 ->
X1 is -B/(2*A),
write('Jedno miejsce zerowe: '), write(X1), nl;
Delta<0 ->
write('Program nie obsluguje funkcji z delta ujemna. Delta wynosi: '),
write(Delta), nl
).

% --------Fakty----------- 
mezczyzna(jan).
mezczyzna(pawel).
mezczyzna(marek).

kobieta(anna).
kobieta(kasia).
kobieta(ola).

rodzic(jan, kuba).
rodzic(jan, kasia).
rodzic(anna, kuba).
rodzic(anna, kasia).
rodzic(pawel, marek).
rodzic(ola, marek).
rodzic(zbyszek, pawel).
rodzic(zbyszek, anna).
rodzic(helena, pawel).
rodzic(helena, anna).

wiek(zbyszek, 70).
wiek(helena, 68).
wiek(jan, 40).
wiek(anna, 50).
wiek(pawel, 40).
wiek(ola, 38).
wiek(marek, 10).
wiek(kasia, 35).


% ---------Reguły:-----------
% rodzic(X,Y) - X jest rodzicem Y
ojciec(X, Y) :- rodzic(X, Y), mezczyzna(X).
matka(X, Y) :- rodzic(X, Y), kobieta(X).

% dziecko(X,Y) - X jest dzieckiem Y
dziecko(X, Y) :- rodzic(Y, X).
syn(X, Y) :- dziecko(X, Y), mezczyzna(X).
corka(X, Y) :- dziecko(X, Y), kobieta(X).

% rodzenstwo(X,Y) - X jest rodzeństwem Y
brat(X, Y) :- mezczyzna(X), X \= Y, rodzic(P, X), rodzic(P, Y).
siostra(X, Y) :- kobieta(X), X \= Y, rodzic(P, X), rodzic(P, Y).

dziadek(X, Y) :- mezczyzna(X), rodzic(X, Z), rodzic(Z, Y).
babcia(X, Y) :- kobieta(X), rodzic(X, Z), rodzic(Z, Y).

wujek(X, Y) :- mezczyzna(X), rodzic(P, Y), rodzic(G, P), rodzic(G, X), X \= P.
ciocia(X, Y) :- kobieta(X), rodzic(P, Y), rodzic(G, P), rodzic(G, X), X \= P.

kuzyn(X, Y) :- mezczyzna(X), rodzic(A, X), rodzic(B, Y), A \= B, rodzic(G, A), rodzic(G, B).
kuzynka(X, Y) :- kobieta(X), rodzic(A, X), rodzic(B, Y), A \= B, rodzic(G, A), rodzic(G, B).

przodek(X, Y) :- rodzic(X, Y) ; (rodzic(X, Z), przodek(Z, Y)).
potomek(X, Y) :- rodzic(Y, X) ; (rodzic(Y, Z), potomek(X, Z)).

glowa_rodu(X) :- mezczyzna(X),\+ rodzic(_, X).

jest_starszy(X, Y) :- wiek(X, WX), wiek(Y, WY), WX > WY.
jest_mlodszy(X, Y) :- wiek(X, WX), wiek(Y, WY), WX < WY.

najstarszy(X) :- wiek(X, WX), \+ (wiek(_, WY), WY > WX).
najmlodszy(X) :- wiek(X, WX), \+ (wiek(_, WY), WY < WX).

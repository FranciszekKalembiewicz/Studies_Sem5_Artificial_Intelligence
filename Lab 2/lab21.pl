% --------Fakty----------- 
% Osoby i wiek
osoba(ala, 28).
osoba(bartosz, 35).
osoba(celia, 22).
osoba(darek, 40).
osoba(ela, 30).

% osoba X mieszka bezpośrednio nad osobą Y
mieszka_nad(ala, celia).
mieszka_nad(bartosz, ala).
mieszka_nad(darek, bartosz).
mieszka_nad(ela, darek).

% osoba X mieszka bezpośrednio pod osobą Y
mieszka_pod(celia, ala).
mieszka_pod(ala, bartosz).
mieszka_pod(bartosz, darek).
mieszka_pod(darek, ela).

% ---------Reguły:-----------
% mieszka_wyzej(X,Y)
mieszka_wyzej(X, Y) :- mieszka_nad(X, Y).
mieszka_wyzej(X, Y) :- mieszka_nad(X, Z), mieszka_wyzej(Z, Y).

% mieszka_nizej(X,Y)
mieszka_nizej(X, Y) :- mieszka_pod(Y, X).
mieszka_nizej(X, Y) :- mieszka_pod(Z, X), mieszka_nizej(Z, Y).

% mieszka_najwyzej(X)
mieszka_najwyzej(X) :- osoba(X, _), \+ mieszka_wyzej(_, X).

% mieszka_najnizej(X)
mieszka_najnizej(X) :- osoba(X, _), \+ mieszka_nizej(_, X).

% jest_starsza(X,Y)
jest_starsza(X, Y) :- osoba(X, WX), osoba(Y, WY), WX > WY.

% jest_mlodsza(X,Y)
jest_mlodsza(X, Y) :- osoba(X, WX), osoba(Y, WY), WX < WY.

% jest_najstarsza(X)
jest_najstarsza(X) :- osoba(X, WX), \+ ( osoba(_, WY), WY > WX ).

% jest_najmlodsza(X)
jest_najmlodsza(X) :- osoba(X, WX), \+ ( osoba(_, WY), WY < WX ).
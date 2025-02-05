 assign(N,C) :- color(C), node(N), not nassign(N,C).
nassign(N,C) :- color(C), node(N), not  assign(N,C).
assigned(N) :- assign(N,C).
:- node(N), not assigned(N).
:- assign(N,C1), assign(N,C2), C1 != C2.
:- edge(N,M), assign(N,C), assign(M,C).

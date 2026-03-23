company(sumsum).
company(appy).

competitor_of(sumsum,appy).
competitor_of(X,Y):-
    competitor_of(Y,X).

boss_of(stevey,appy).

business(X):-
    smart_phone_technology(X).

smart_phone_technology(galactica-s3).

steal(stevey,galactica-s3,sumsum).

rival(X,Y):-
    company(X),
    company(Y),
    competitor_of(X,Y).

unethical(Boss):-
    steal(Boss,Business,Other),
    boss_of(Boss,Company),
    rival(Company,Other),
    business(Business).
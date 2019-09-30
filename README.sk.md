# Testovacia platforma pre správu pamäte
V tomto projekte je vytvorená nová testovacia platforma, určená na vyhodnotenie algoritmov dynamického prideľovania pamäte v rámci systémov v reálneho času. Platforma, vytvára štatistiky o alokačných algoritmoch. Súčasťou tejto platformy je aj grafické užívateľské rozhranie, ktoré sa spúšťa na externom počítači pripojenom k ​​testovacej platforme. Platforma vykonáva testovanie podľa rôznych predpripravených testovacích scenárov. Ako hardvér sa používa mikropočítač Arduino Uno. Výsledky testov sa odosielajú cez USB-UART do externého počítača, kde sa výsledky zobrazujú v aplikácii s GUI. Hlavným cieľom novej testovacej platformy je schopnosť vyhodnotiť rôzne nové algoritmy prideľovania pamäte a ich implementácie a porovnať ich atribúty a výkon s inými existujúcimi algoritmami. Okrem toho bude počas vykonávania testovacích scenárov možné sledovať zmeny v pamäti online. Z dôvodu opakovaného prideľovania a uvoľňovania pamäťových blokov rôznych veľkostí a miest je možné pozorovať, ako sa v pamäti objaví fragmentácia. Na koniec je tiež možné porovnávať rôzne metódy a algoritmy prideľovania pamäte podľa ich časov odozvy a determinizmu.


## Architektúra testovacej platformy

![Alt text](img/architecture.png?raw=true "Architecture of testing platform")

## Grafické používateľské rozhranie

![Alt text](img/gui.png?raw=true "Gui")


# Testovacia platforma pre správu pamäte
V tomto projekte je vytvorená nová testovacia platforma, určená na vyhodnotenie algoritmov dynamického prideľovania pamäte v rámci systémov v reálneho času. Platforma, vytvára štatistiky o alokačných algoritmoch. Súčasťou tejto platformy je aj grafické užívateľské rozhranie, ktoré sa spúšťa na externom počítači pripojenom k ​​testovacej platforme. Platforma vykonáva testovanie podľa rôznych predpripravených testovacích scenárov. Ako hardvér sa používa mikropočítač Arduino Uno. Výsledky testov sa odosielajú cez USB-UART do externého počítača, kde sa výsledky zobrazujú v aplikácii s GUI. Hlavným cieľom novej testovacej platformy je schopnosť vyhodnotiť rôzne nové algoritmy prideľovania pamäte a ich implementácie a porovnať ich atribúty a výkon s inými existujúcimi algoritmami. Okrem toho bude počas vykonávania testovacích scenárov možné sledovať zmeny v pamäti online. Z dôvodu opakovaného prideľovania a uvoľňovania pamäťových blokov rôznych veľkostí a miest je možné pozorovať, ako sa v pamäti objaví fragmentácia. Na koniec je tiež možné porovnávať rôzne metódy a algoritmy prideľovania pamäte podľa ich časov odozvy a determinizmu.

Na základe tohto projektu bol publikovaný vedecký článok na konferencii IIT.SRC 2017. 

## Architektúra testovacej platformy

![Alt text](img/architecture.png?raw=true "Architecture of testing platform")

Testovacia platforma sa skladá z dvoch častí, pričom prvá časť beží na minipočítači Arduino MEGA 2560 a druhá na externom počítači. Prvá využíva operačný systém FreeRTOS a rozširuje ho o algoritmy správy pamäte. Tieto sú implementované v rovnakom jazyku ako operačný systém FreeRTOS a teda jazyku C. 
Druhá časť, ktorá obsahuje grafické používateľské rozhranie a je spustená na externom počítači, je implementovaná v jazyku Python 2.7. 

Na vytvorenie dizajnu grafického rozhrania bol použitý Qt Designer, pomocou ktorého sa vygeneroval xml súbor a ten sa následne prekonvertoval do Pythonu.


## Grafické používateľské rozhranie

![Alt text](img/gui.png?raw=true "Gui")

## Implementácia algoritmov
V rámci projektu sme vytvorili a porovnali implementácie dvoch algoritmov správy pamäte: Best fit a Worst fit.

Pre správne a rýchle fungovanie oboch algoritmov je potrebné mať uložené voľné bloky pamäte v dátovej štruktúre, ktorá ich udržiava usporiadané v správnom poradí. V prípade algoritmu Best fit je usporiadanie voľných blokov od najmenšieho po najväčší. V prípade algoritmu Worst fit od najväčšieho po najmenší. Bloky označujúce začiatok a koniec pamäťového priestoru sú tiež uložené v tejto dátovej štruktúre ale v žiadnom prípade nie sú použité ako hlavička nového bloku.

Jeden blok pamäte je dátová štruktúra, ktorá predstavuje hlavičku bloku pamäte. Obsahuje tri údaje. Typ týchto údajov závisí od pamäte, v ktorej bude daná implementácia pracovať. Ich význam ale v každom prípade ostáva rovnaký. Sú to tieto:
* ukazovateľ (adresa) na nasledujúci voľný blok
* ukazovateľ (adresa) na predchádzajúci fyzický blok
* veľkosť bloku




## Licencia
Tento projekt bol vytvorený v rámci bakalárskej práce na FIIT STU. Máj 2017.


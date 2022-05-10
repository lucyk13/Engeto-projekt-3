# Engeto-projekt-3

Projekt číslo 3 pro kurz Python Academy od Engeto

Program vytáhne výsledky voleb z roku 2017 přímo z webu pro určitý územní celek a zapíše výsledky do souboru .csv. 
Do souboru zapíše údaje: kód obce, název obce, voliče v seznamu, vydané obálky, platné hlasy, kandidující strany a pro jednodušší kontrolu také odkaz.

Projekt obsahuje:
  - soubor s programem (election_scraper_lk.py)
  - soubor se seznamem knihoven a verzí (requirements.txt)
  - tuto stručnou dokumentaci
  - soubor s uloženým výstupem (pro ukázku: benesov.csv)

Nejdříve je nutno nainstalovat knihovny ze seznamu. V tomto případě requests a beautifulsoup.
Pro instalaci pomocí pip v terminálu: 
pip install beautifulsoup4 
pip install requests


Soubor potřebuje pro pro správný běh 2 argumenty při spuštění. 

Jako první argument musí být zadána webová stránka pro kterou mají být zpracováný výsledky voleb (v této ukázce pro Benešov: "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101")
Jako druhý argument musí být zadán název souboru do kterého se mají zapsat výsledky ve formátu .csv (v této ukázce "benesov.csv")


Program nejdříve zkontroluje zadané parametry. 
Průběžně vypíše i pro kontrolu počty získaných hodnot.
Nakonec vše zapíše do souboru .csv

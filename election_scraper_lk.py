#!/usr/bin/env python3
import csv
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from itertools import zip_longest


def najdi_cely_html(url):
    r = requests.get(url)
    html = BeautifulSoup(r.text, "html.parser")

    return html


def najdi_kod_obce(html):
    kody_obce = html.find_all("td", {"class": "cislo"})
    kody_obce_list = []
    for elem in kody_obce:
        text = elem.text
        kody_obce_list.append(text)

    return kody_obce_list


def najdi_jmena_obce(html):
    jmena_obce = html.find_all("td", {"class": "overflow_name"})
    jmena_obce_list = []
    for elem in jmena_obce:
        text = elem.text
        jmena_obce_list.append(text)

    return jmena_obce_list


def najdi_odkazy(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    odkazy_list = []

    for td in soup.findAll("td", {"class": "center"}):
        for a in td.findAll("a", {"href": True}):
            href = urljoin(url, a["href"])
            odkazy_list.append(href)

    return odkazy_list

def najdi_pododkazy(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    odkazy_list = []

    for td in soup.findAll("td", {"class": "cislo"}):
        for a in td.findAll("a", {"href": True}):
            href = urljoin(url, a["href"])
            odkazy_list.append(href)

    return odkazy_list


def najdi_volice(odkazy):
    vsechno_list = []
    html = najdi_cely_html(odkazy)
    for cislo  in html.find_all("td", {"class": "cislo"}, {"headers": "sa3"}):
        text = cislo.text
        vsechno_list.append(text)
    volic = vsechno_list[3]

    return volic

def najdi_pod_volice(odkazy):
    vsechno_list = []
    html = najdi_cely_html(odkazy)
    for cislo  in html.find_all("td", {"class": "cislo"}, {"headers": "sa2"}):
        text = cislo.text
        novy_text = text.replace('\xa0', '').encode("utf-8")

        vsechno_list.append(novy_text)
    volic = vsechno_list[0]

    return volic

def najdi_pod_obalky(odkazy):
    vsechno_list = []
    html = najdi_cely_html(odkazy)
    for cislo  in html.find_all("td", {"class": "cislo"}, {"headers": "sa3"}):
        text = cislo.text
        novy_text = text.replace('\xa0', '').encode("utf-8")

        vsechno_list.append(novy_text)
    obalka = vsechno_list[1]

    return obalka

def najdi_pod_hlasy(odkazy):
    vsechno_list = []
    html = najdi_cely_html(odkazy)
    for cislo  in html.find_all("td", {"class": "cislo"}, {"headers": "sa6"}):
        text = cislo.text
        novy_text = text.replace('\xa0', '').encode("utf-8")

        vsechno_list.append(novy_text)
    hlas = vsechno_list[4]

    return hlas

def najdi_obalky(odkazy):
    vsechno_list = []
    html = najdi_cely_html(odkazy)
    for cislo  in html.find_all("td", {"class": "cislo"}, {"headers": "sa3"}):
        text = cislo.text
        vsechno_list.append(text)

    obalka = vsechno_list[4]

    return obalka

def najdi_hlasy(odkazy):
    vsechno_list = []
    html = najdi_cely_html(odkazy)
    for cislo  in html.find_all("td", {"class": "cislo"}, {"headers": "sa3"}):
        text = cislo.text
        vsechno_list.append(text)
    hlas = vsechno_list[7]

    return hlas


def najdi_strany(odkazy):
    vsechno_list = []
    html = najdi_cely_html(odkazy)
    for elem in html.find_all("td", {"class": "overflow_name"}):
        text = elem.text
        vsechno_list.append(text)

    return vsechno_list

def zapis_do_souboru(data_list, output_path):
    fieldnames = ["kody", "jmena_obci", "odkazy", "volici_list", "obalky_list", "hlasy_list", "strany_list"]

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames, delimiter=",")
        writer.writeheader()
        for row_dict in data_list:
            writer.writerow(row_dict)
    return writer


#_____________________________________________________________________
def main():
    starting_url = sys.argv[1]
    output = sys.argv[2]

    if "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj" not in sys.argv[1]:
        print("Webová stránka musí být použita jako první argument. Případně je špatně zadaný vstupní web. \n Ukončuji program.")
        sys.exit(1)

    elif ".csv" not in output:
        print("Název výstupního souboru musí být použit jako druhý argument. Případně je špatně zadaný název souboru. Musí být ve formátu .csv \n Ukončuji program.")
        sys.exit(2)

    else:
        print(f"Vstupní web je: {starting_url}, název souboru je: {output} \n")

    html = najdi_cely_html(starting_url)
    uvod = html.find_all("h3")
    kraj = uvod[0].text
    okres = uvod[1].text
    print(f"Zpracovávám údaje pro: \n{kraj}{okres}")

    kody = najdi_kod_obce(html)
    jmena_obci = najdi_jmena_obce(html)
    odkazy = najdi_odkazy(starting_url)

    pocet_obci_kody = len(kody)
    pocet_obci_jmena = len(jmena_obci)
    pocet_obci_odkazy = len(odkazy)
    #print(f"Pocet kodu je: {pocet_obci_kody}, pocet jmen je: {pocet_obci_jmena}, pocet odkazu je {pocet_obci_odkazy} \n ")

    print(f"Počet obcí v okresu je {pocet_obci_kody}.")
    print(f"Nalezených hodnot s kódem obce je: {pocet_obci_kody}")
    print(f"Nalezených hodnot se jménem obce je: {pocet_obci_jmena}")

    if pocet_obci_jmena == pocet_obci_kody == pocet_obci_odkazy:
        print("Stránka se načetla v pořádku.\nPokračuji...\n")
    else:
        print("Něco nefunguje.\n")

    podokrsky = []
    for i in range(0, len(odkazy)):
        html = najdi_cely_html(odkazy[i])
        elem = html.text
        if "Okrsek" in elem:
            podokrsky.append("vice podokrsku")
        else:
            podokrsky.append("nejsou")

    pocet = len(podokrsky)
    print(f"Počet zkontrolovaných obcí na okrsky je {pocet}")
    pocet_s_pododkazy = podokrsky.count("vice podokrsku")
    print(f"Z celkového počtu obcí: {pocet} jich je s okrsky: {pocet_s_pododkazy} \n")
    print("Procházím obce a jejich okrsky...")


    volici_list = []
    obalky_list = []
    hlasy_list = []
    strany_list = []
    pododkazy = []
    adresy = []

    for i in range (0, len(podokrsky)):
        if podokrsky[i] == "nejsou":
            volici = najdi_volice(odkazy[i])
            volici_list.append(volici)

            obalky = najdi_obalky(odkazy[i])
            obalky_list.append(obalky)

            hlasy = najdi_hlasy(odkazy[i])
            hlasy_list.append(hlasy)

            strany = najdi_strany(odkazy[i])
            strany_list.append(strany)

        else:
            pododkazy.append(odkazy[i])
            adresy = najdi_pododkazy(odkazy[i])
            pocet = len(adresy)

            podvolici = []
            for i in range (0, pocet):
                volici = najdi_pod_volice(adresy[i])
                volic = int(volici)
                podvolici.append(volic)

            celkem_volicu = sum(podvolici)
            volici_list.append(celkem_volicu)

            podobalky = []
            for i in range (0, len(adresy)):
                obalky = najdi_pod_obalky(adresy[i])
                obalka = int(obalky)
                podobalky.append(obalka)
            celkem_obalek = sum(podobalky)
            obalky_list.append(celkem_obalek)

            podhlasy = []
            for i in range (0, len(adresy)):
                hlasy = najdi_pod_hlasy(adresy[i])
                hlas = int(hlasy)
                podhlasy.append(hlas)
            celkem_hlasu = sum(podhlasy)
            hlasy_list.append(celkem_hlasu)

            for i in range (0, len(adresy)):
                strany = najdi_strany(adresy[i])
            strany_list.append(strany)

    pocet_volicu = len(volici_list)
    print(f"Nalezených hodnot s počtem voličů v seznamu je: {pocet_volicu}")
    pocet_obalek = len(obalky_list)
    print(f"Nalezených hodnot s počtem odevzdaných obálek je: {pocet_obalek}")
    pocet_hlasu = len(hlasy_list)
    print(f"Nalezených hodnot s počtem platných hlasů je: {pocet_hlasu}")
    pocet_stran = len(strany_list)
    print(f"Nalezených hodnot s počtem seznamů stran je: {pocet_stran}\n")

    d = [kody, jmena_obci, volici_list, obalky_list, hlasy_list, strany_list, odkazy]
    export_data = zip_longest(*d, fillvalue="")

    with open(output, "w", encoding="utf-8", newline="") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy", "Strany", "odkaz"))
        wr.writerows(export_data)

        print(f"Výsledky zapisuji do souboru {output}")

    myfile.close()


if __name__ == "__main__":
    sys.exit(main())
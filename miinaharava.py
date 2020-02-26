import haravasto as h
import random as r
import time as t
import timeit
import datetime


tila = {
    "peliruutu": [],
    "piiloruutu": [],
    "HAVIO": False,
    "VOITTO": False,
    "SIIRROT": 0,
    "MIINAT": 0,
    "AIKA_ALKU": 0,
    "AIKA_LOPPU": 0
}
piiloruutu = [
]
peliruutu = [
]
start = 0
stop = 0

def piirra_kentta():

    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    h.tyhjaa_ikkuna()
    h.piirra_tausta()
    h.aloita_ruutujen_piirto()
    for y, j in enumerate(peliruutu):
        for x, i in enumerate(j):
            h.lisaa_piirrettava_ruutu(i,  x*40, y*40)
    h.piirra_ruudut()

def ruudukointi(ruutu, leveys, korkeus,):
    for rivi in range(0, korkeus):
        ruutu.append([])
        for sarake in range(0, leveys):
            ruutu[-1].append(" ")
    return ruutu

def liputa(rx, ry):
    
    if peliruutu[ry][rx] == piiloruutu[ry][rx]:
        pass
    else:
        if peliruutu[ry][rx] == "f":
            peliruutu[ry][rx] = " "
        else:
            peliruutu[ry][rx] = "f"



def kasittele_hiiri(x, y, nappi, muokkausnappain):
    if tila["HAVIO"] == False and tila["VOITTO"] == False:
        rx = int(x / 40)
        ry = int(y / 40)
        if nappi == h.HIIRI_VASEN:
            tila["SIIRROT"] += 1
            tulvataytto(rx, ry)
            tarkasta_samat()
            tilastointi()
            if tila["HAVIO"] == True:
                print("Hävisit pelin... Klikkaa mitä tahansa jatkaaksesi...")
            elif tila["VOITTO"] == True: 
                print("Voitit pelin! Klikkaa mitä tahansa jatkaaksesi...")
        elif nappi == h.HIIRI_OIKEA:
            tarkasta_samat()
            liputa(rx, ry)
            tilastointi()
            if tila["HAVIO"] == True:
                print("Hävisit pelin... Klikkaa mitä tahansa jatkaaksesi...")
            elif tila["VOITTO"] == True: 
                print("Voitit pelin! Klikkaa mitä tahansa jatkaaksesi...")
    elif tila["HAVIO"] == True or tila["VOITTO"] == True:
        h.lopeta()

def tarkasta_samat():
    samoja = 0
    kaikki = 0

    for x, i in enumerate(piiloruutu):
        for y, j in enumerate(i):
            kaikki += 1
    print(kaikki)
    for x, i in enumerate(peliruutu):
        for y, j in enumerate(i):
            if peliruutu[x][y] == piiloruutu[x][y]:
                samoja += 1
    print(samoja)
    voitettava = kaikki - tila["MIINAT"]
    print(voitettava)
    
    if samoja == voitettava:
        print("voitit")
        tila["VOITTO"] = True

'''
    tyhjia = 0
    for y in peliruutu:
        for x in y:
            if x == " ":
                tyhjia += 1
    if tyhjia == tila["MIINAT"]:
        tila["VOITTO"] = True
'''
def nayta_miinat():
    for x, i in enumerate(piiloruutu):
        for y, j in enumerate(i):
            if piiloruutu[x][y] == "x":
                peliruutu[x][y] = "x"


def tulvataytto(x_aloitus, y_aloitus):
    koordinaatit = [[x_aloitus, y_aloitus]]
    korkeus = len(peliruutu) - 1
    leveys = len(peliruutu[0]) - 1
    if piiloruutu[y_aloitus][x_aloitus] == "x":
        peliruutu[y_aloitus][x_aloitus] = piiloruutu[y_aloitus][x_aloitus]
        tila["HAVIO"] = True
        nayta_miinat()
    elif peliruutu[y_aloitus][x_aloitus] == "f":
        return   
    elif piiloruutu[y_aloitus][x_aloitus] == "0":
        while koordinaatit:
            piste = koordinaatit.pop()
            x = piste[0]
            y = piste[1]
            peliruutu[piste[1]][piste[0]] = "0"
            if x == 0:
                xalku = x
                xloppu = x + 1
            elif x == leveys:
                xalku = x - 1
                xloppu = x
            else:
                xalku = x - 1
                xloppu = x + 1
            if y == 0: 
                yalku = y
                yloppu = y + 1
            elif y == korkeus:
                yalku = y - 1
                yloppu = y
            else:
                yalku = y - 1
                yloppu = y + 1
            for y in range(yalku, yloppu + 1):
                for x in range(xalku, xloppu + 1):
                    if peliruutu[y][x] == peliruutu[piste[1]][piste[0]]:
                        pass
                    elif peliruutu[y][x] == "f":
                        pass
                    else:
                        if piiloruutu[y][x] == "0":
                            koordinaatit.append((x, y))
                        
                        else:
                            peliruutu[y][x] = piiloruutu[y][x]
    else:
        peliruutu[y_aloitus][x_aloitus] = piiloruutu[y_aloitus][x_aloitus]

def tilastointi():
    if tila["HAVIO"] == False and tila["VOITTO"] == False:
        return
    elif tila["HAVIO"] == True:
        printattava = "Häviö"
    elif tila["VOITTO"] == True:
        printattava = "Voitto"
    tila["AIKA_LOPPU"] = timeit.default_timer()
    kulunut_aika = int(tila["AIKA_LOPPU"] - tila["AIKA_ALKU"])
    tilastot = str(datetime.datetime.now()), "Miinoja:" + str(tila["MIINAT"]), "Siirtoja:" + str(tila["SIIRROT"]), "Aikaa kului:" + str(kulunut_aika) + "s", printattava
    with open("miinatilastot.txt", "r+") as file:
        sisus = file.readlines() 
        sisus = list(reversed(sisus))
        while len(sisus) >= 10:
            sisus.pop()
        sisus = list(reversed(sisus))
        sisus.append(str(tilastot) + "\n")
    with open("miinatilastot.txt", "w") as newfile:
        uusisisus = "".join(sisus)
        newfile.write(uusisisus)


def miinoita(kentta, jaljella, miinat):
    for miina in range(miinat):
        x, y = r.choice(jaljella)
        jaljella.remove((x, y))
        kentta[y][x] = "x"


def laske_numerot(kentta, korkeus, leveys):
    for y in range(0, korkeus):
        for x in range(0, leveys):
            lkm = laske_ninjat(x, y, kentta)
            if kentta[y][x] != "x":
                kentta[y][x] = str(lkm) 
     
def laske_ninjat(x, y, huone):
    ninjat = 0
    korkeus = len(huone) - 1
    leveys = len(huone[0]) - 1

    if x == 0:
        xalku = x
        xloppu = x + 1
    elif x == leveys:
        xalku = x - 1
        xloppu = x
    else:
        xalku = x - 1
        xloppu = x + 1

    if y == 0: 
        yalku = y
        yloppu = y + 1
    elif y == korkeus:
        yalku = y - 1
        yloppu = y
    else:
        yalku = y - 1
        yloppu = y + 1


    for x in range(xalku, xloppu + 1):
        for y in range(yalku, yloppu + 1):
            if huone[y][x] == "x":
                ninjat += 1
    return ninjat            

def alustus():
    print("Alustetaan...")
    tila["VOITTO"] = False
    tila["HAVIO"] = False
    piiloruutu.clear()
    peliruutu.clear()
    tila["SIIRROT"] = 0
    tila["MIINAT"] = 0
    start = 0
    stop = 0

def kysely():
    leveys = 5 #int(input("Anna kentän leveys: "))
    korkeus = 5 #int(input("Anna kentän korkeus: "))
    miinat = 2 #int(input("Montako miinaa?: "))
    return leveys, korkeus, miinat
        

def laske_jaljella(leveys, korkeus):
    jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))
    return jaljella

def main():
    alustus()
    tila["AIKA_ALKU"] = timeit.default_timer()
    leveys, korkeus, miinat = kysely()
    tila["MIINAT"] = miinat
    ruudukointi(piiloruutu, leveys, korkeus)
    ruudukointi(peliruutu, leveys, korkeus)
    jaljella = laske_jaljella(leveys, korkeus)
    miinoita(piiloruutu, jaljella, miinat)
    laske_numerot(piiloruutu, korkeus, leveys)
    h.lataa_kuvat("spritet")
    h.luo_ikkuna(leveys * 40, korkeus * 40)
    h.aseta_piirto_kasittelija(piirra_kentta)
    h.aseta_hiiri_kasittelija(kasittele_hiiri)
    h.aloita()

if __name__ == '__main__':
    main()
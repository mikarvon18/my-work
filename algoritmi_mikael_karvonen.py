import time
groups = [] #tallennetaan kaikki minimivirittävän puun välit

tiedosto = "H:/TT/TRA/graph_large_testdata_2/graph_ADS2018_200.txt"

def main():
	lista = []
	tic = time.perf_counter()
	with open(tiedosto) as f: #tallennetaan listaan kaikki rivit tekstitiedostosta
		for line in f:
				lista.append([int(x) for x in line.split()])
	dest = lista[-1][0] #määritellään määränpää
	lista.pop()
	lista.remove(lista[0])
	notvisited = []
	for i in range(1, dest + 1):
		notvisited.append(i)

	reitit = sorted(lista, key=lambda lista: lista[-1]) #reitit -listaan tallennetaan kaikki reitit järjestyksessä pienimmästä korkeudesta suurimpaan
	union(reitit, notvisited) #yhdistetään jokainen piste johonkin polkuun
	ryhma = []
	for i in range(1, dest + 1):
		ryhma.append(i)

	index = 0
	liittyvat = [[]] #tähän tallennetaan kaikki polut(esim. [1->2->3], [4->5->6], ...)
	while len(ryhma) > 0:
		etsiliittyvat(index, liittyvat, ryhma) #haetaan toisiinsa liittyvät polut (esim. {[1->2], [2->3]} => {1->2->3})
		index += 1
	jaljella = [] #tähän tallennetaan kaikki reitit joita ei ole vielä "käytetty"
	for i in reitit:
		if i not in groups:
			jaljella.append(i)
	while len(liittyvat) > 1:
		minimipuu(liittyvat, jaljella, reitit) #haetaan kaikkia polkuja yhdistävät reitit
	lkm = len(groups)

	minimireitit = sorted(groups, key=lambda lista: groups[-1])
	minimipolku = minimireitti(dest, minimireitit) #haetaan minimiviritetystä puusta reitti 1 -> dest
	if minimipolku:
		korkeus = minimipolku.pop()
		print(f"Lopullinen polku: {minimipolku}, maksimikorkeus: {korkeus}")
	else:
		print("Ei polkua")
	toc = time.perf_counter()
	print(f"Haku kesti {toc - tic:0.4f} sekuntia")

def minimireitti(dest, minimireitit):
	"""
	Haetaan lopullisesta minimiviritetystä puusta reitti 1 -> dest käymällä kaikki reitit läpi
	"""
	index = 0
	polut = [[1]]
	for i in minimireitit:             #haetaan ensin kaikki 1:stä lähtevät reitit
		if i[0] == 1:
			polut.append([1])
			polut[index].append(i[1])
			polut[index].append(i[2])
			index += 1

	polut.pop()
	for i in polut:
		for j in minimireitit:
			reitti = i[:]
			if i[-2] == j[0] and j[1] not in i:
				reitti.insert(-1, j[1])
				if j[-1] > reitti[-1]:
					reitti[-1] = j[-1]
				polut.append(reitti)
			elif i[-2] == j[1] and j[0] not in i:
				reitti.insert(-1, j[0])
				if j[-1] > reitti[-1]:
					reitti[-1] = j[-1]
				polut.append(reitti)
	for i in polut:
		if i[0] == 1 and i[-2] == dest:
			return i
	return False
	

def minimipuu(liittyvat, jaljella, reitit):
	"""
	Haetaan kahta polkua yhdistävä reitti ja yhdistetään polut, sekä lisätään reitti groups -listaan. esim. 
	[[1,2,3,4],[5,6,7]], yhdistää reitti [4,5]. Reitti [4,5] lisätään listaan ja luodaan uusi polku: [1,2,3,4,5,6,7]
	"""
	for i in jaljella:
		for j in liittyvat:
			if (i[0] in j and i[1] not in j): #jos tutkittavan reitin alku, ja loppu eivät jo ole samassa polussa, niin i on
																			   #pienin reitti, joka yhdistää jotkin kaksi polkua
				yhdistava = i
				groups.append(yhdistava)
				yhdista(yhdistava, liittyvat)

def yhdista(yhdistava, liittyvat):
	"""
	Haetaan ne kaksi polkua, jotka aiemmin löydetty reitti yhdistää, sekä tehdään niistä yksi uusi polku.
	"""
	for i in liittyvat:
		if yhdistava[0] in i:
			yhdistettava1 = i
		elif yhdistava[1] in i:
			yhdistettava2 = i
	yhdistetty = yhdistettava1 + yhdistettava2
	liittyvat.remove(yhdistettava1)
	liittyvat.remove(yhdistettava2)
	liittyvat.append(yhdistetty)

def union(reitit, notvisited):
	"""
	Yhdistetään kaksi pistettä toisiinsa
	"""
	for i in reitit:
		reitti = i[:]
		for j in range(0, len(reitti) - 1):

			if reitti[j] in notvisited:
				if reitti not in groups:
					groups.append(reitti)
				notvisited.remove(i[j])


def etsiliittyvat(index, liittyvat, ryhma):
	"""
	Etsitään toisiinsa liittyvät polut esim. {[1,2],[2,3],[3,4] -> [1,2,3,4]}
	"""
	pienin = ryhma[0]
	ryhma.remove(pienin)
	liittyvat[index].append(pienin)
	for i in liittyvat[index]:
		for j in groups:
			if i == j[0] and j[1] not in liittyvat[index]:
				liittyvat[index].append(j[1])
				if j[1] in ryhma:
					ryhma.remove(j[1])
			elif i == j[1] and j[0] not in liittyvat[index]:
				liittyvat[index].append(j[0])
				if j[0] in ryhma:
					ryhma.remove(j[0])
	if len(ryhma) > 0:
		liittyvat.append([])

if __name__ == '__main__':
	main()
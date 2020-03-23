""" Problema de cautare (mesaj intre elevii unei clase) """


def pozitionare(matrice):
    poz = {}  # Dictionar in care retinem pozitiile fiecarui elev
    # retinem perechi (i,j)
    for i in range(m):  # Matricea e n*m
        for j in range(n):
            poz[matrice[i][j][0]] = (0, i, j)  # Sta in stanga in banca
            poz[matrice[i][j][1]] = (1, i, j)  # Sta in dreapta in banca
    if "liber" in poz:
        del poz["liber"]
    return poz


class Configuratie:  # Constructor de copiere pentru matrice
    def __init__(self, pozitie_bilet):
        self.pozitie_bilet = pozitie_bilet

    def __repr__(self):
        return f"{self.pozitie_bilet}"

    def __eq__(self, other):
        return self.pozitie_bilet == self.pozitie_bilet

    def euristica(self):
        # O sa verificam daca pozitia biletului si pozitia copilului la care
        # trebuie sa ajunga biletul sunt pe aceeasi coloana, daca nu sunt trebuie sa trecem
        # pe alta coloana si asta se face doar pe ultimul si penultimul rand

        # ignoram locurile libere si supararile

        global poz_primire  # Pozitia elevului care trebuie sa primeasca biletul
        global n  # nr coloane, care este mereu 3
        global m  # nr randuri
        poz_bilet = self.pozitie_bilet

        # Distanta Manhattan: abs(x1- x2) + abs(y1 – y2)
        if (poz_bilet[2] == poz_primire[2]):  # sunt pe acelasi rand

            if(poz_bilet[0] == poz_primire[0]):  # daca sunt in stanga in banca
                return abs(poz_bilet[1] - poz_primire[1]) + abs(poz_bilet[2] - poz_primire[2])
            else:  # unul sta in stang si unul sta in dreapta
                return abs(poz_bilet[1] - poz_primire[1]) + abs(poz_bilet[2] - poz_primire[2]) + 1

        else:  # sunt pe randuri diferite
            # Transferul se face doar pe la ultima si penultima banca

            # Din locul in care e biletul trebuie sa mearga la penultima banca
            dif_pozB_penultima_banca = abs(m - 2 - poz_bilet[1])
            dif_pozD_penultima_banca = abs(m - 2 - poz_primire[1])

            # diferenta de un rand intre ele
            if abs(poz_primire[2] - poz_bilet[2]) == 1:
                if poz_primire[0] == poz_bilet[0]:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 1
                else:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 2

            if abs(poz_primire[2] - poz_bilet[2]) == 2:  # diferenta de 2 randuri
                if poz_primire[0] == poz_bilet[0]:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 3
                else:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 4


class Nod:
    def __init__(self, config):
        self.info = config
        self.h = config.euristica()

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self, capat, varf, cost):
        self.capat = capat
        self.varf = varf
        self.cost = cost


class Problema:
    def __init__(self):
        self.noduri = [Nod(configuratie_initiala)]
        self.arce = []
        self.nod_start = self.noduri[0]
        self.nod_scop = poz_primire  # Pun pozitia finala a biletului

    def cauta_nod_nume(self, info):
        """Stiind doar informatia "info" a unui nod,
        trebuie sa returnati fie obiectul de tip Nod care are acea informatie,
        fie None, daca nu exista niciun nod cu acea informatie."""
        # TO DO ... DONE
        for nod in self.noduri:
            if nod.info == info:
                return nod
        return None


""" Sfarsit definire problema """


""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
            Cuprinde o referinta catre nodul in sine (din graf)
            dar are ca proprietati si valorile specifice algoritmului A* (f si g).
            Se presupune ca h este proprietate a nodului din graf

    """

    problema = None  # atribut al clasei

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf  	# obiect de tip Nod
        self.parinte = parinte  	# obiect de tip Nod
        self.g = g  	# costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        """
                Functie care calculeaza drumul asociat unui nod din arborele de cautare.
                Functia merge din parinte in parinte pana ajunge la radacina
        """
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        """
                Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
                Verificarea se face mergand din parinte in parinte pana la radacina
                Se compara doar informatiile nodurilor (proprietatea info)
                Returnati True sau False.

                "nod" este obiect de tip Nod (are atributul "nod.info")
                "self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
        """
        # TO DO ... DONE
        nod_c = self
        while nod_c.parinte is not None:
            if nod.info.pozitie_bilet == nod_c.nod_graf.info.pozitie_bilet:
                return True
            nod_c = nod_c.parinte
        return False

    # se modifica in functie de problema

    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.(Fiecare tuplu contine un obiect d
        e tip Nod si un numar.)
        """

        # Daca avem destinatarul pe coloana 1 si primitorul pe 3, trebuie pe coloana 2 doar sa trecem pe ultima sau penultima banca
        # fara sa ne ridicam in sus

        global matrice_clasa  # Matricea cu numele
        global pozitii_in_banci  # Dictionar
        poz_bilet = self.nod_graf.info.pozitie_bilet  # (st/dr,i,j)
        succ = []

        # Un copil din pozitia curenta poate da biletul in fata in spate si la colegul de banca
        # Trebuie sa nu uitam ca mai sunt locuri libere si copii suparati nu trimit mesajul intre ei

        # Colturile trebuie tratate separat
        # Schimbatul cu ultima/ penultima banca

        # Verificam daca poate sa ii dea colegului de banca, daca nu sunt suparati sau e loc liber
        if poz_bilet[0] == 0:  # e in st
            banca = matrice_clasa[poz_bilet[1]][poz_bilet[2]]
            if banca[1] != "liber":
                # Daca nu sunt suparati
                if not ((banca[0], banca[1]) in suparati or (banca[1], banca[0]) in suparati):
                    conf_noua = Configuratie((1, poz_bilet[1], poz_bilet[2]))
                    succ.append((Nod(conf_noua), 1))

            # Schimbam randul si noi suntem in st
            if (poz_bilet[1] == m - 2 or poz_bilet[1] == m - 1) and poz_bilet[2] != 0:
                # Banca pe care urmeaza sa ne mutam
                # cu o coloana mai in stanga
                banca = matrice_clasa[poz_bilet[1]][poz_bilet[2]-1]
                if banca[1] != "liber":
                    # Daca nu sunt suparati
                    if not ((matrice_clasa[poz_bilet[1]][poz_bilet[2]][0], banca[1]) in suparati or (banca[1], matrice_clasa[poz_bilet[1]][poz_bilet[2]][0]) in suparati):
                        conf_noua = Configuratie(
                            (1, poz_bilet[1], poz_bilet[2]-1))
                        succ.append((Nod(conf_noua), 1))

        else:  # e in dreapta
            banca = matrice_clasa[poz_bilet[1]][poz_bilet[2]]
            if banca[0] != "liber":
                    # Daca nu sunt suparati
                if not ((banca[0], banca[1]) in suparati or (banca[1], banca[0]) in suparati):
                    conf_noua = Configuratie((0, poz_bilet[1], poz_bilet[2]))
                    succ.append((Nod(conf_noua), 1))

            # Schimbam randul si noi suntem in dr
            if (poz_bilet[1] == m - 2 or poz_bilet[1] == m - 1) and poz_bilet[2] != n-1:
                # Banca pe care urmeaza sa ne mutam cu o coloana mai in dreapta
                banca = matrice_clasa[poz_bilet[1]][poz_bilet[2]+1]
                if banca[0] != "liber":
                    # Daca nu sunt suparati
                    if not ((matrice_clasa[poz_bilet[1]][poz_bilet[2]][0], banca[1]) in suparati or (banca[1], matrice_clasa[poz_bilet[1]][poz_bilet[2]][0]) in suparati):
                        conf_noua = Configuratie(
                            (0, poz_bilet[1], poz_bilet[2]+1))
                        succ.append((Nod(conf_noua), 1))

        # Verificam daca putem da la ala din fata sau spate
        if poz_bilet[1] - 1 >= 0:  # in jos
            if matrice_clasa[poz_bilet[1] - 1][poz_bilet[2]][poz_bilet[0]] != "liber":
                conf_noua = Configuratie(
                    (poz_bilet[0], poz_bilet[1] - 1, poz_bilet[2]))
                succ.append((Nod(conf_noua), 1))
        if poz_bilet[1] + 1 < m:  # in sus
            if matrice_clasa[poz_bilet[1] + 1][poz_bilet[2]][poz_bilet[0]] != "liber":
                conf_noua = Configuratie(
                    (poz_bilet[0], poz_bilet[1]+1, poz_bilet[2]))
                succ.append((Nod(conf_noua), 1))
        return succ

    def test_scop(self):
        return self.nod_graf.info.pozitie_bilet == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
            o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for k in range(1, len(l)):
        # Nod curent
        poz = l[k].nod_graf.info.pozitie_bilet[0]  # st/dr in banca
        i = l[k].nod_graf.info.pozitie_bilet[1]
        j = l[k].nod_graf.info.pozitie_bilet[2]

        # Parinte
        poz_parinte = i_parinte = l[k-1].nod_graf.info.pozitie_bilet[0]
        i_parinte = l[k-1].nod_graf.info.pozitie_bilet[1]
        j_parinte = l[k - 1].nod_graf.info.pozitie_bilet[2]

        if not sir:
            if poz_parinte == 0:
                sir += matrice_clasa[i_parinte][j_parinte][0] + " "
            else:
                sir += matrice_clasa[i_parinte][j_parinte][1] + " "

        # Colegi de banca
        if i == i_parinte and j == j_parinte:
            if poz == 0:  # copilul curent sta in st, deci ne-am mutam din dreapta
                sir += "< "
            else:  # copilul curent sta in dr, deci ne-am mutam in st
                sir += "> "

        # Sus sau jos
        if i > i_parinte and j == j_parinte:
            sir += "v "
        if i < i_parinte and j == j_parinte:
            sir += "^ "

        # Trecem pe randul urmator
        if j > j_parinte and i == i_parinte:
            sir += ">> "
        if j < j_parinte and i == i_parinte:
            sir += "<< "

        if poz == 0:
            sir += matrice_clasa[i][j][0] + " "
        else:
            sir += matrice_clasa[i][j][1] + " "
    return sir


def afis_succesori_cost(l):
    """
            o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: "+str(x)+", cost arc:" + str(cost) + "\n"
    return sir


def in_lista(l, nod):
    """
            lista "l" contine obiecte de tip NodParcurgere
            "nod" este de tip Nod
    """
    for i in range(len(l)):
        if l[i].nod_graf.info.pozitie_bilet == nod.info.pozitie_bilet:
            return l[i]
    return None


def a_star():
    """
        Functia care implementeaza algoritmul A-star
    """

    nod_curent = None

    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere

    while len(open) > 0:
        print(str_info_noduri(open))  # afisam lista open
        nod_curent = open.pop(0)  # scoatem primul element din lista open
        closed.append(nod_curent)  # si il adaugam la finalul listei closed

        # testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
        if nod_curent.test_scop():
            break

        l_succesori = nod_curent.expandeaza()  # contine tupluri de tip (Nod, numar)
        for (nod_succesor, cost_succesor) in l_succesori:
            # "nod_curent" este tatal, "nod_succesor" este fiul curent

            # daca fiul nu e in drumul dintre radacina si tatal sau (adica nu se creeaza un circuit)
            if not nod_curent.contine_in_drum(nod_succesor):

                nod_nou = None

                # calculez valorile g si f pentru "nod_succesor" (fiul)
                # g-ul tatalui + cost muchie(tata, fiu)
                g_succesor = nod_curent.g + cost_succesor
                f_succesor = g_succesor + nod_succesor.h  # g-ul fiului + h-ul fiului

                # verific daca "nod_succesor" se afla in closed
                # (si il si sterg, returnand nodul sters in nod_parcg_vechi
                nod_parcg_vechi = in_lista(closed, nod_succesor)

                if nod_parcg_vechi is not None:  # "nod_succesor" e in closed
                    # daca g-ul calculat pentru drumul actual este mai bun (mai mic) decat
                    #        g-ul pentru drumul gasit anterior (g-ul nodului aflat in lista closed)
                    # atunci actualizez parintele, g si f
                    # si apoi voi adauga "nod_nou" in lista open
                    if g_succesor < nod_parcg_vechi.g:
                        # scot nodul din lista closed
                        closed.remove(nod_parcg_vechi)
                        nod_parcg_vechi.parinte = nod_curent  # actualizez parintele
                        nod_parcg_vechi.g = g_succesor  # actualizez g
                        nod_parcg_vechi.f = f_succesor  # actualizez f
                        nod_nou = nod_parcg_vechi  # setez "nod_nou", care va fi adaugat apoi in open

                else:
                    # daca nu e in closed, verific daca "nod_succesor" se afla in open
                    nod_parcg_vechi = in_lista(open, nod_succesor)

                    if nod_parcg_vechi is not None:  # "nod_succesor" e in open
                        # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                        #        f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista open)
                        # atunci scot nodul din lista open
                        #         (pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
                        # actualizez parintele, g si f
                        # si apoi voi adauga "nod_nou" in lista open (la noua pozitie corecta in sortare)
                        if f_succesor < nod_parcg_vechi.f:
                            open.remove(nod_parcg_vechi)
                            nod_parcg_vechi.parinte = nod_curent
                            nod_parcg_vechi.g = g_succesor
                            nod_parcg_vechi.f = f_succesor
                            nod_nou = nod_parcg_vechi

                    else:  # cand "nod_succesor" nu e nici in closed, nici in open
                        nod_nou = NodParcurgere(
                            nod_graf=nod_succesor, parinte=nod_curent, g=g_succesor)
                        # se calculeaza f automat in constructor

                if nod_nou:
                    # inserare in lista sortata crescator dupa f
                    # (si pentru f-uri egale descrescator dupa g)
                    i = 0
                    while i < len(open):
                        if open[i].f < nod_nou.f:
                            i += 1
                        else:
                            while i < len(open) and open[i].f == nod_nou.f and open[i].g > nod_nou.g:
                                i += 1
                            break

                    open.insert(i, nod_nou)

    print("\n------------------ Concluzie -----------------------")
    if len(open) == 0:
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))


# Input
n = 3  # Sunt 3 coloane de banci, cate 7 elevi pe rand
matrice_clasa = [
    [("ionel", "alina"), ("teo", "eliza"), ("carmen", "monica")],
    [("george", "diana"), ("bob", "liber"), ("nadia", "mihai")],
    [("liber", "costin"), ("anda", "bogdan"), ("dora", "marin")],
    [("luiza", "simona"), ("dana", "cristian"), ("tamara", "dragos")],
    [("mihnea", "razvan"), ("radu", "patricia"), ("gigel", "elena")],
    [("liber", "andrei"), ("oana", "victor"), ("liber", "dorel")],
    [("viorel", "alex"), ("ela", "nicoleta"), ("maria", "gabi")]
]

m = len(matrice_clasa)  # 7, numarul de randuri
# ionel ii trimite mesaj lui dragos

mesaj_trimis_de = "ionel"
mesaj_primit_de = "dragos"
pozitii_in_banci = pozitionare(matrice_clasa)  # Dictionar

poz_destinatar = pozitii_in_banci[mesaj_trimis_de]
poz_primire = pozitii_in_banci[mesaj_primit_de]
configuratie_initiala = Configuratie(poz_destinatar)

suparati = [("george", "ionel"), ("ela", "nicoleta"), ("victor", "oana"),
            ("teo", "eliza"), ("teo", "luiza"), ("elena", "dragos"), ("alina", "dragos")]


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()

# Nu-i bine ca nu-mi face drumul minim
# cand ajunge pe randul 2 se urca in sus nu trece spre dreapta

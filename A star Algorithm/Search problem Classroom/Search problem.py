""" Problema de cautare (mesaj intre elevii unei clase) """

import time
import math

# Declarare
numar_euristica = None  # Numarul euristicii pe care o folosim
n = None  # Numar coloane
m = None  # Numar linii
matrice_clasa = None  # Matricea cu elevi
mesaj_trimis_de = None  # Numele celui care trimite mesajul
mesaj_primit_de = None  # Numele celui care primeste mesajul
pozitii_in_banci = None  # Un dictionar cu pozitiile elevilor in banci
poz_destinatar = None  # Pozitia celui care trimite biletul
poz_primire = None  # Pozitia celui care trebuie sa primeasca biletul
configuratie_initiala = None  # Configuratia initiala, pozitia biletului la inceput
suparati = None  # Lista cu elevi suparati
fisier_output = None  # Fisierul in care scriem rezultatele


def pozitionare(matrice):
    poz = {}  # Dictionar in care retinem pozitiile fiecarui elev
    # retinem perechi (st/dr, i, j) st=0, dr=1
    for i in range(m):  # Matricea e n*m
        for j in range(n):
            poz[matrice[i][j][0]] = (0, i, j)  # Sta in stanga in banca
            poz[matrice[i][j][1]] = (1, i, j)  # Sta in dreapta in banca
    if "liber" in poz:  # Stergem "liber"
        del poz["liber"]
    return poz


class Configuratie:
    def __init__(self, pozitie_bilet):
        self.pozitie_bilet = pozitie_bilet  # (0/1, i, j) 0-stanga, 1-dreapta

    def __repr__(self):
        return f"{self.pozitie_bilet}"

    def __eq__(self, other):
        return self.pozitie_bilet == self.pozitie_bilet

    def euristica(self, numar_euristica):
        if numar_euristica == 1:
            return self.euristica1()
        elif numar_euristica == 2:
            return self.euristica2()
        elif numar_euristica == 3:
            return self.euristica3()

    def euristica1(self):
        """Distanta Manhattan este cea mai mica distant care poate fi parcursa intre 2 puncte.
        Prin urmare, distanta Manhattan va fi mereu mai mica sau egala decat adevarata distanta ce trebuie parcursa
        de bilet pentru a putea ajunge la pozitia finala (0 ≤ h(n) ≤ h*(n)). In plus, daca nu ar exista
        elevi suparati sau locuri libere, distanta Manhattan ar fi egala cu adevarata distanta.
        In concluzie, euristica este consistenta, iar orice euristica consistenta este si admisibila."""

        # O sa verificam daca pozitia biletului si pozitia copilului la care
        # trebuie sa ajunga biletul sunt pe aceeasi coloana, daca nu sunt trebuie sa trecem
        # pe alta coloana si asta se face doar pe ultimul si penultimul rand

        # ignoram locurile libere si supararile

        global poz_primire  # Pozitia elevului care trebuie sa primeasca biletul
        global n  # nr coloane, care este mereu 3
        global m  # nr randuri
        poz_bilet = self.pozitie_bilet

        # Distanta Manhattan: abs(x1- x2) + abs(y1 – y2)
        if (poz_bilet[2] == poz_primire[2]):  # sunt pe aceeasi coloana

            if(poz_bilet[0] == poz_primire[0]):  # daca sunt in stanga in banca
                return abs(poz_bilet[1] - poz_primire[1]) + abs(poz_bilet[2] - poz_primire[2])
            else:  # unul sta in stang si unul sta in dreapta
                return abs(poz_bilet[1] - poz_primire[1]) + abs(poz_bilet[2] - poz_primire[2]) + 1

        else:  # sunt pe coloane diferite
            # Transferul se face doar pe la ultima si penultima banca

            # Din locul in care e biletul trebuie sa mearga la penultima banca
            dif_pozB_penultima_banca = abs(m - 2 - poz_bilet[1])
            dif_pozD_penultima_banca = abs(m - 2 - poz_primire[1])

            # diferenta de o coloane intre ele, adica 1 sau 2 coloane in clasa
            if abs(poz_primire[2] - poz_bilet[2]) == 1:
                if poz_primire[0] == poz_bilet[0]:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 1
                else:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 2

            # diferenta de 2 coloane, adica 3-4 coloane in clasa
            if abs(poz_primire[2] - poz_bilet[2]) == 2:
                if poz_primire[0] == poz_bilet[0]:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 3
                else:
                    return dif_pozD_penultima_banca + dif_pozB_penultima_banca + 4

    def euristica2(self):
        """Distanta Euclidiana este cea mai mica distant care poate fi parcursa intre 2 puncte.
        Prin urmare, distanta Euclidiana va fi mereu mai mica sau egala decat adevarata distanta ce trebuie parcursa
        de bilet pentru a putea ajunge la pozitia finala (0 ≤ h(n) ≤ h*(n)). In plus, daca nu ar exista
        elevi suparati sau locuri libere, distanta Euclidiana ar fi egala cu adevarata distanta.
        In concluzie, euristica este consistenta, iar orice euristica consistenta este si admisibila."""
        # O sa verificam daca pozitia biletului si pozitia copilului la care
        # trebuie sa ajunga biletul sunt pe aceeasi coloana, daca nu sunt trebuie sa trecem
        # pe alta coloana si asta se face doar pe ultimul si penultimul rand

        # ignoram locurile libere si supararile

        global poz_primire  # Pozitia elevului care trebuie sa primeasca biletul
        global n  # nr coloane, care este mereu 3
        global m  # nr randuri
        poz_bilet = self.pozitie_bilet

        # Distanta Euclidiana: sqrt(abs(x1- x2)^2 + abs(y1 – y2)^2)
        if (poz_bilet[2] == poz_primire[2]):  # sunt pe aceeasi coloana

            if(poz_bilet[0] == poz_primire[0]):  # daca sunt in stanga in banca
                return math.sqrt((abs(poz_bilet[1] - poz_primire[1])) ** 2 + (abs(poz_bilet[2] - poz_primire[2]) ** 2))
            else:  # unul sta in stang si unul sta in dreapta
                return math.sqrt(
                    (abs(poz_bilet[1] - poz_primire[1])) ** 2 + (abs(poz_bilet[2] - poz_primire[2] + 1) ** 2))

        else:  # sunt pe coloane diferite
            # Transferul se face doar pe la ultima si penultima banca

            # Din locul in care e biletul trebuie sa mearga la penultima banca
            dif_pozB_penultima_banca = abs(m - 2 - poz_bilet[1])
            dif_pozD_penultima_banca = abs(m - 2 - poz_primire[1])

            # diferenta de o coloana intre ele, adica 1-2 coloane in clasa
            if abs(poz_primire[2] - poz_bilet[2]) == 1:
                if poz_primire[0] == poz_bilet[0]:
                    return math.sqrt((dif_pozD_penultima_banca + dif_pozB_penultima_banca) ** 2 + 1 ** 2)
                else:
                    return math.sqrt((dif_pozD_penultima_banca + dif_pozB_penultima_banca) ** 2 + 2 ** 2)

            # diferenta de 2 coloane, adica 3-4 coloane in realitate
            if abs(poz_primire[2] - poz_bilet[2]) == 2:
                if poz_primire[0] == poz_bilet[0]:
                    return math.sqrt((dif_pozD_penultima_banca + dif_pozB_penultima_banca) ** 2 + 3 ** 2)
                else:
                    return math.sqrt((dif_pozD_penultima_banca + dif_pozB_penultima_banca) ** 2 + 4 ** 2)

    def euristica3(self):
        """Euristica 3 nu este o euristica admisibila, deoarece suma a mai multor euristici admisibile nu este o euristica admisibila
        si am obligat algoritmul sa treaca pe coloana urmatoare doar pe la ultima banca.
        Euristica este incosistenta, deoarce cand pozitia biletului este pe ultimul sau penultimul rand 
        returnam o valoare care nu respecta monotonia."""
        global poz_primire  # Pozitia elevului care trebuie sa primeasca biletul
        global n  # nr coloane, care este mereu 3
        global m  # nr randuri
        poz_bilet = self.pozitie_bilet
        if abs(poz_primire[2] - poz_bilet[2]) != 0:
            # Il facem sa prefere sa treaca pe alta coloana pe ultimul rand
            if poz_bilet[1] == m - 2:
                return (self.euristica1() + self.euristica2()) ** 10
            if poz_bilet[1] == m - 1:
                return 0
        return self.euristica1() + self.euristica2()


class Nod:
    def __init__(self, config):
        self.info = config
        self.h = config.euristica(numar_euristica)

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
        # fara sa ne ridicam in sus, doar daca e necesar(locuri libere sau suparati)

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

    def test_scop(self):  # testez daca nodul extras din lista open este nod scop
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


def a_star(f):
    """
        Functia care implementeaza algoritmul A-star
    """

    # preiau timpul in milisecunde de dinainte de A*
    t_inainte = int(round(time.time() * 1000))

    nod_curent = None

    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere

    while len(open) > 0:
        # f.write(str_info_noduri(open)+"\n")  # afisam lista open
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

    # Concluzie
    # scrie_output(nod_curent, open)
    if len(open) == 0:
        if mesaj_primit_de == mesaj_trimis_de:
            f.write(
                f"Lista open e vida, mesajul este deja la {mesaj_primit_de}\n")
        else:
            f.write(
                f"Lista open e vida, nu avem drum de la {mesaj_trimis_de} la {mesaj_primit_de}\n")
    else:
        f.write("Drum de cost minim: " +
                str_info_noduri(nod_curent.drum_arbore())+"\n")

    # preiau timpul in milisecunde de dupa A*
    t_dupa = int(round(time.time() * 1000))
    f.write("Calculatorul a \"gandit\" timp de " +
            str(t_dupa - t_inainte) + " milisecunde.\n\n")


def citire_input():
    global n
    global m
    global matrice_clasa
    global mesaj_trimis_de
    global mesaj_primit_de
    global pozitii_in_banci
    global poz_destinatar
    global poz_primire
    global configuratie_initiala
    global suparati
    global nume_fisier_input

    # Deschidem fisierul de input
    f = open(nume_fisier_input, "r")

    # Pe primul rand avem numele celui care trimite mesajul si numele celui care trebuie sa primeasca
    linie = f.readline().split()
    mesaj_trimis_de = linie[0]
    mesaj_primit_de = linie[1]

    # Numar linii si numar coloane
    linie = f.readline().split()
    m = (int)(linie[0])  # randuri
    # Pun cate doi in banci, adica fac o matrice 7x3 si elemenetele sunt tupluri (colegii de banca)
    n = ((int)(linie[1]))//2  # coloane

    # Matricea cu asezarea in banci
    matrice_clasa = [[0 for x in range(n)] for y in range(m)]
    for i in range(m):
        linie = f.readline().split()
        k = 0
        for j in range(n):
            matrice_clasa[i][j] = (linie[k], linie[k + 1])
            k += 2

    # Numarul de perechi de suparati
    linie = f.readline().split()
    nr_perechi_suparati = (int)(linie[0])

    # Perechile de suparati
    suparati = [0 for i in range(nr_perechi_suparati)]
    for i in range(nr_perechi_suparati):
        linie = f.readline().split()
        suparati[i] = (linie[0], linie[1])


if __name__ == "__main__":
    # Meniu pentru accesarea meniului
    text = "Alegeti numarul inputului dorit:\n"
    text += "1. Un fisier de input care nu are solutii\n"
    text += "2. Un fisier de input care da o stare initiala care este si finala\n"
    text += "3. Un fisier de input cu un drum de cost minim de lungime 3-5\n"
    text += "4. Un fisier de input cu un drum de cost minim de lungime mai mare decat 5\n"
    print(text)

    # Repetam primim un raspuns valid
    raspuns_valid = False
    while not raspuns_valid:
        global nume_fisier_input
        tip_algoritm = input(
            "Varianta input: ")
        if tip_algoritm in ['1', '2', '3', '4']:
            raspuns_valid = True
            if tip_algoritm == '1':
                nume_fisier_input = "input1.txt"
                fisier_output = "output1.txt"
            elif tip_algoritm == '2':
                nume_fisier_input = "input2.txt"
                fisier_output = "output2.txt"
            elif tip_algoritm == '3':
                nume_fisier_input = "input3.txt"
                fisier_output = "output3.txt"
            elif tip_algoritm == '4':
                nume_fisier_input = "input4.txt"
                fisier_output = "output4.txt"
        else:
            print("Nu ati ales o varianta corecta.")

    # Apelam Algoritmul A* pentru toate euristicile

    # Citire input
    citire_input()

    # Dictionar cu pozitiile in banci
    pozitii_in_banci = pozitionare(matrice_clasa)

    # Numele celui care trimite mesajul si numele celui care trebuie sa primeasca
    poz_destinatar = pozitii_in_banci[mesaj_trimis_de]
    poz_primire = pozitii_in_banci[mesaj_primit_de]

    # Deschide fisierul de output
    f = open(fisier_output, "w")

    # Pentru fiecare euristica apelam Algoritmul A*
    f.write("\n------------------ Concluzie -----------------------\n")

    # Algoritmul A* pentru euristica 1
    numar_euristica = 1
    # Configuratia initiala
    configuratie_initiala = Configuratie(poz_destinatar)
    problema = Problema()
    NodParcurgere.problema = problema
    a_star(f)

    # Algoritmul A* pentru euristica 2
    numar_euristica = 2
    # Configuratia initiala
    configuratie_initiala = Configuratie(poz_destinatar)
    problema = Problema()
    NodParcurgere.problema = problema
    a_star(f)

    # Algoritmul A* pentru euristica 3
    numar_euristica = 3
    # Configuratia initiala
    configuratie_initiala = Configuratie(poz_destinatar)
    problema = Problema()
    NodParcurgere.problema = problema
    a_star(f)

    # Inchidem output-ul
    f.close()


"Problema blocurilor"


class Configuratie:
    def __init__(self, stive):
        self.stive = stive

    def __repr__(self):
        return f"{self.stive}"

    def __eq__(self, other):
        return self.stive == other.stive

    def pozitionare(self):
        # Dictionar in care retinem (i,j), litera cub se afla pe stiva i pozitia j
        poz = {}
        for i, turn in enumerate(self.stive):
            for j, cub in enumerate(turn):
                poz[cub] = (i, j)
        return poz

    def euristica(self):
        global poz_scop  # Dictionar cu configuratia la care trebuie sa ajungem
        distanta = 0
        poz = self.pozitionare()  # pozitiile cuburilor din configuratie

        # Parcurgem cub-urile
        for cub in cuburi:
            if poz[cub] != poz_scop[cub]:
                distanta += 1
        return distanta


class Nod:
    def __init__(self, config):
        self.info = config
        self.h = config.euristica()

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self, capat, varf):
        self.capat = capat
        self.varf = varf
        self.cost = 1  # Toate mutarile au costul 1


class Problema:
    def __init__(self):
        self.noduri = [Nod(config_initiala)]
        self.arce = []
        self.nod_start = self.noduri[0]
        self.nod_scop = config_scop

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
            if nod.info == nod_c.nod_graf.info:
                return True
            nod_c = nod_c.parinte
        return False

    # se modifica in functie de problema

    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.
        (Fiecare tuplu contine un obiect de tip Nod si un numar.)
        """
        # TO DO ... DONE
        configuratie = self.nod_graf.info  # stiva de stive
        succ = []
        for ind_stiva_curenta in range(nr_stive):
            for ind_stiva_destinatie in range(nr_stive):
                if ind_stiva_curenta == ind_stiva_destinatie:
                    continue  # Nu mutam un cub pe aceeasi stiva

                # Daca e stiva vida, nu facem mutari, nu avem ce muta
                if not configuratie.stive[ind_stiva_curenta]:
                    continue

                # ultimul cub
                cub_de_mutat = configuratie.stive[ind_stiva_curenta][-1]

                stive_noi = []
                for i in range(nr_stive):
                    if i == ind_stiva_curenta:
                        # Nu pune si cubul extras, cel de mutat
                        stiva_noua = configuratie.stive[i][:-1]
                    elif i == ind_stiva_destinatie:
                        stiva_noua = configuratie.stive[i] + [cub_de_mutat]
                    else:
                        stiva_noua = configuratie.stive[i]
                    stive_noi.append(stiva_noua)

                configuratie_noua = Configuratie(stive_noi)

                # Verificam daca nu am explorat deja aceasta configuratie
                succesor = problema.cauta_nod_nume(configuratie_noua)

                if not succesor:  # Daca n-am mai explorat configuratia noua, o adaugam in arbore
                    nod_nou = Nod(configuratie_noua)
                    problema.noduri.append(nod_nou)
                    succesor = nod_nou

                cost = 1  # Toate mutarile au costul 1
                succ.append((succesor, cost))

        return succ

    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
            o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = "["
    for x in l:
        sir += str(x) + "\n"
    sir += "]\n"
    return sir


def afis_succesori_cost(l):
    """
            o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: "+str(x)+", cost arc:" + str(cost)
    return sir


def in_lista(l, nod):
    """
            lista "l" contine obiecte de tip NodParcurgere
            "nod" este de tip Nod
    """
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None


def a_star():
    """
            Functia care implementeaza algoritmul A-star
    """
    # TO DO ... DONE

    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere
    nod_nou = None

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
            if (not nod_curent.contine_in_drum(nod_succesor)):

                # calculez valorile g si f pentru "nod_succesor" (fiul)
                # g-ul tatalui + cost muchie(tata, fiu)
                g_succesor = nod_curent.g + cost_succesor
                f_succesor = g_succesor + nod_succesor.h  # g-ul fiului + h-ul fiului

                # verific daca "nod_succesor" se afla in closed
                # (si il si sterg, returnand nodul sters in nod_parcg_vechi
                nod_parcg_vechi = in_lista(closed, nod_succesor)

                if nod_parcg_vechi is not None:  # "nod_succesor" e in closed
                    # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                    # 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista closed)
                    # atunci actualizez parintele, g si f
                    # si apoi voi adauga "nod_nou" in lista open
                    if (f_succesor < nod_parcg_vechi.f):
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
                        # 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista open)
                        # atunci scot nodul din lista open
                        # 		(pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
                        # actualizez parintele, g si f
                        # si apoi voi adauga "nod_nou" in lista open (la noua pozitie corecta in sortare)
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
nr_stive = 3
nr_cuburi = 4
cuburi = ['a', 'b', 'c', 'd']
config_initiala = Configuratie([['a'], ['b', 'c'], ['d']])
config_scop = Configuratie([['b', 'c'], [], ['d', 'a']])
poz_scop = config_scop.pozitionare()

if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()

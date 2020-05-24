# Dame

import time
import copy

import sys


def move(matrice, pozitie, d, jucator):
    # pozitia = pozitia noua
    # d[0] - element din vectorul de directii
    # d[1] - pozitia veche
    # facem mutarea si scotem piesele pe care le sarim

    # Transormam toate piesele pe care le gasim in drumul nostru de la pozitia noua la pozitia veche in loc gol ("#")
    i_nou, j_nou = pozitie[0], pozitie[1]
    i_nou -= d[0][0]
    j_nou -= d[0][1]  # Mergem spre pozitia veche
    i_vechi = d[1][0]
    j_vechi = d[1][1]
    matrice[i_vechi][j_vechi] = Joc.GOL
    while i_nou != i_vechi and j_vechi != j_nou:
        # Transformam semnele de pe drum in loc gol, "#"
        matrice[i_nou][j_nou] = Joc.GOL
        i_nou -= d[0][0]
        j_nou -= d[0][1]

    if jucator == Joc.SIMBOLURI_JOC[0]:  # n
        if pozitie[0] == 0:
            jucator = jucator.upper()  # il facem rege
    elif jucator == Joc.SIMBOLURI_JOC[1]:  # a
        if pozitie[0] == Joc.NR_LINII-1:
            jucator = jucator.upper()  # il facem rege

    i_nou, j_nou = pozitie[0], pozitie[1]
    matrice[i_nou][j_nou] = jucator  # Piesa pusa in pozitia noua


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII = 8
    SIMBOLURI_JOC = ['n', 'a']
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):  # Initializare
        if tabla is not None:
            self.matr = tabla  # matrice
        else:
            self.matr = [[Joc.GOL for _ in range(
                Joc.NR_COLOANE)] for _ in range(Joc.NR_LINII)]
            for i in range(Joc.NR_LINII):
                if i < 3:
                    for j in range((i+1) % 2, Joc.NR_COLOANE, 2):
                        self.matr[i][j] = self.SIMBOLURI_JOC[1]
                if i >= 5:
                    for j in range((i+1) % 2, Joc.NR_COLOANE, 2):
                        self.matr[i][j] = self.SIMBOLURI_JOC[0]

    def final(self, jucator):
        # returnam simbolul jucatorului castigator daca nu mai exista mutari posibile
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat jocul

        pos = self.posibilitati(jucator)
        if len(pos) == 0:  # Daca nu mai sunt mutari posibile
            # Scorul este numarul de piese negre - numarul de piese albe
            scor_jmin = self.nr_piese(self.JMIN)
            scor_jmax = self.nr_piese(self.JMAX)
            self.print_scor()
            if scor_jmin == 0:  # returnam simbolul castigator, jucatoru care inca mai are piese
                return self.JMAX
            elif scor_jmax == scor_jmin:
                return 'remiza'
            else:
                return self.JMIN
        return False

    def posibilitati(self, jucator):
        # returneaza un dictionar: cheile sunt pozitiile in care se pot pune piese
        #                          (directie, pozitie veche)
        pos = {}
        # Jucator opus
        if jucator == self.SIMBOLURI_JOC[0] or jucator == self.SIMBOLURI_JOC[0].upper():
            jucator_opus = self.SIMBOLURI_JOC[1]
        if jucator == self.SIMBOLURI_JOC[1] or jucator == self.SIMBOLURI_JOC[1].upper():
            jucator_opus = self.SIMBOLURI_JOC[0]

        # Toate deplasarile se pot realiza doar pe diagoala

        # Daca piesa este rege(idiferent de culoare), atunci poate sa mearga in ambele directii
        directii = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Daca e piesa alba, atunci poate sa mearga doar in jos pe diagonala
        if jucator == self.SIMBOLURI_JOC[0]:
            directii = [(-1, -1), (-1, 1)]

        # Daca e piesa neagra, atunci poate sa mearga doar in sus pe diagonala
        if jucator == self.SIMBOLURI_JOC[1]:
            directii = [(1, -1), (1, 1)]

        i_final = j_final = -1

        if True:
            for i in range(self.NR_LINII):
                for j in range(self.NR_COLOANE):
                    if self.matr[i][j].upper() == jucator.upper():
                        # Daca piesa este rege(idiferent de culoare), atunci poate sa mearga in ambele directii
                        directii = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

                        # Daca e piesa alba, atunci poate sa mearga doar in jos pe diagonala
                        # jucator nu e rege
                        if self.matr[i][j] == self.SIMBOLURI_JOC[0]:  # n
                            directii = [(-1, -1), (-1, 1)]

                        # Daca e piesa neagra, atunci poate sa mearga doar in sus pe diagonala
                        # jucator nu e rege
                        if self.matr[i][j] == self.SIMBOLURI_JOC[1]:  # a
                            directii = [(1, -1), (1, 1)]

                        for directie in directii:
                            i_nou, j_nou = i + directie[0], j + directie[1]

                            if i_nou not in range(self.NR_LINII) or j_nou not in range(self.NR_COLOANE) \
                                    or self.matr[i_nou][j_nou].upper() == jucator.upper():  # Daca noua pozitie nu e in interval si e o piesa la fel pusa acolo
                                continue

                            ok = 0
                            # Cazul in care se duce din prima pe o piesa libera
                            if self.matr[i_nou][j_nou] == self.GOL:
                                gasit = True
                                ok = 0  # daca a fost din prima pe loc gol

                            # Cazul in care sare mai multe piese
                            else:
                                ok = 1
                                gasit = True
                                i_gol, j_gol = i_nou + \
                                    directie[0], j_nou + directie[1]
                                if i_nou in range(self.NR_LINII) and j_nou in range(self.NR_COLOANE) and \
                                        i_gol in range(self.NR_LINII) and j_gol in range(self.NR_COLOANE) \
                                        and self.matr[i_nou][j_nou].upper() == jucator_opus.upper() and self.matr[i_gol][j_gol] == self.GOL:

                                    # trebuie sa avem perechi piesa jucator opus + loc gol
                                    while self.matr[i_nou][j_nou].upper() == jucator_opus.upper() and self.matr[i_gol][j_gol] == self.GOL:
                                        # Mergem din 2 in 2 cu piesa opusa
                                        i_final = i_gol
                                        j_final = j_gol
                                        i_nou = i_gol + directie[0]
                                        j_nou = j_gol + directie[1]
                                        i_gol, j_gol = i_nou + \
                                            directie[0], j_nou + directie[1]
                                        if i_nou not in range(self.NR_LINII) or j_nou not in range(self.NR_COLOANE) or self.matr[i_nou][j_nou].upper() == jucator.upper() or \
                                                i_gol not in range(self.NR_LINII) or j_gol not in range(self.NR_COLOANE) or self.matr[i_gol][j_gol] != self.GOL:
                                            break
                                else:
                                    gasit = False

                            if ok == 1:  # Pozitiile noi sunt cele care au ramas in i/j_final
                                i_nou = i_final
                                j_nou = j_final

                            if gasit:  # (directie, poz_veche)
                                if (i_nou, j_nou) not in pos.keys():
                                    pos[(i_nou, j_nou)] = [(directie, (i, j))]
                                else:
                                    pos[(i_nou, j_nou)].append(
                                        (directie, (i, j)))  # o piesa poate avea mai multe mutari disponibile
        return pos

    def mutari(self, jucator):
        l_mutari = []  # Mutarile urmatoare, tabla de joc copiata si adaugata noua mutare

        posibilitati = self.posibilitati(jucator)  # Mutarile posibile
        for pozitie, dirs in posibilitati.items():
            for d in dirs:
                matr_noua = copy.deepcopy(self.matr)  # Copiem matricea curenta
                # ce tip de piesa este la pozitie d[1](pozitia veche)
                jucator_tip = matr_noua[d[1][0]][d[1][1]]
                move(matr_noua, pozitie, d, jucator_tip)  # Facem mutarea
                l_mutari.append(Joc(matr_noua))  # Adaugam noua tabla in lista
        return l_mutari

    def nr_piese(self, jucator):  # Calculam numarul de piese a unui jucator
        nr = 0
        for line in self.matr:
            nr += line.count(jucator)
            nr += line.count(jucator.upper())
        return nr

    # Calculam valoarea pieselor unui jucator pentru euristica
    def nr_piese_euristica(self, jucator):
        # pion=1, rege=2
        nr = 0
        for line in self.matr:
            nr += line.count(jucator)
            nr += line.count(jucator.upper())*2  # Regii au valoare dubla
        return nr

    # Calculam valoarea pieselor unui jucator pentru euristica, in functie de pozitia piesei pe tabla
    def val_piese(self, jucator):
        val = 0
        index = 0
        if jucator == 'n':
            for line in self.matr:
                # (valoare_pion + numarul_liniei) * cati pioni sunt pe linie
                val += (5 + index) * line.count(jucator)
                # (valoare_rege + numarul_liniei) * cati pioni sunt pe linie
                val += (10 + index) * line.count(jucator.upper())
                index += 1
        else:
            for line in self.matr: # a
                # (valoare_pion + NR_LINII - numarul_liniei) * cati pioni sunt pe linie
                val += (5 + self.NR_LINII - index) * line.count(jucator)
                # (valoare_rege + NR_LINII - numarul_liniei) * cati pioni sunt pe linie
                val += (10 + self.NR_LINII - index) * line.count(jucator.upper())
                index += 1
        return val

    def print_scor(self):  # Afisare scor
        puncte_jmin = self.nr_piese(Joc.JMIN)  # Numar piese calculator
        puncte_jmax = self.nr_piese(Joc.JMAX)  # Numar piese calculator
        if Joc.JMIN == 'n':
            print(f"Scorul este:  negru: {puncte_jmin}, alb: {puncte_jmax}\n")
        else:
            print(f"Scorul este:  negru: {puncte_jmax}, alb: {puncte_jmin}\n")

    def fct_euristica1(self):
        # Numar piese calculator - Numar piese jucator, indiferent de pozitiile pieselor pe tabla
        # Valori piese Rege=2, Pion=1, deoarce regele are mai multa putere putand merge si inapoi
        return self.nr_piese_euristica(Joc.JMAX) - self.nr_piese_euristica(Joc.JMIN)

    def fct_euristica2(self):
        # Numar piese calculator - Numar piese jucator cu valorile lor
        # Vom lua in considerarea pe ce rand este fiecare pion, deoarce cu cat este mai aproape de marginea tablei jucatorului opus
        # are mai multe sanse sa devina rege si sa fie o piesa mai puternica
        # Valoarea unui pion va fi 5 + randul pe care se afla
        # Valoarea unui rege va fi 10 + randul pe care se afla
        return self.val_piese(Joc.JMAX) - self.val_piese(Joc.JMIN.upper())

    def estimeaza_scor(self, adancime, jucator):  # Estimeaza scorul
        t_final = self.final(jucator)
        if t_final == Joc.JMAX:
            return 999 + adancime
        elif t_final == Joc.JMIN:
            return -999 - adancime
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica1()

    def __str__(self):
        sir = '  '
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + ' '
        sir += '\n'

        for lin in range(self.NR_LINII):
            sir += (str(lin) + ' ' + " ".join([str(x)
                                               for x in self.matr[lin]]) + "\n")
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):  # Jucatorul opus
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # Lista cu mutarile
        juc_opus = self.jucator_opus()  # Jucatorul opus
        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari  # intoarcem lista cu noile stari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent: " + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.scor = stare.tabla_joc.estimeaza_scor(
            stare.adancime, stare.j_curent)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.scor = stare.tabla_joc.estimeaza_scor(
            stare.adancime, stare.j_curent)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta, jucator):  # Afisam daca am terminat jocul
    final = stare_curenta.tabla_joc.final(jucator)
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    # preiau timpul in milisecunde de la inceputul jocului
    t_iceputul_jocului = int(round(time.time() * 1000))

    # Numar total de mutari
    numar_mutari_JMAX = 0  # calculator
    numar_mutari_JMIN = 0  # jucator

    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input(
            "Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input(
            "Alege dificultatea jocului(1, 2 sau 3):\n1. Usor\n2. Mediu\n3. Dificil\n")
        if n.isdigit():
            if n == '1':
                Stare.ADANCIME_MAX = 2
                raspuns_valid = True
            if n == '2':
                Stare.ADANCIME_MAX = 3
                raspuns_valid = True
            if n == '3':
                Stare.ADANCIME_MAX = 4
                raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul intre 1 si 3.")

    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JOC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(
            input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2)))
        if Joc.JMIN in Joc.SIMBOLURI_JOC:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(
        tabla_curenta, Joc.SIMBOLURI_JOC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    linie_veche = -1
    coloana_veche = -1
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if afis_daca_final(stare_curenta, Joc.JMIN):
                break

            # muta jucatorul
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    rasp_valid = False
                    while not rasp_valid:
                        print("Alege 1 sau 2:\n 1. Continua jocul\n 2. Exit\n")
                        raspuns = input("Raspunsul: ")
                        if raspuns == '1':
                            rasp_valid = True
                        if raspuns == '2':
                            stare_curenta.tabla_joc.print_scor()
                            rasp_valid = True
                            sys.exit(0)

                    pos = stare_curenta.tabla_joc.posibilitati(
                        tabla_curenta.JMIN)
                    print("Pozitii posibile: ")
                    for key, values in pos.items():
                        for value in values:
                            s = f"pozitie noua: {key}, pozitie veche: {value[1]}"
                            print(s)
                    print()

                    linie = int(input("linie noua = "))
                    coloana = int(input("coloana noua= "))

                    if (linie, coloana) in pos.keys():

                        # Trebuie sa stiu care dintre piesele care pot ajunge pe aceeasi pozitie trebuie mutata
                        raspuns_valid_vechi = False
                        while not raspuns_valid_vechi:
                            linie_veche = int(input("linie veche = "))
                            coloana_veche = int(input("coloana veche= "))
                            for p in pos[(linie, coloana)]:
                                if (linie_veche, coloana_veche) == p[1]:
                                    raspuns_valid_vechi = True
                                    break
                        raspuns_valid = True
                    else:
                        print("Pozitie invalida. Pozitii posibile: ")
                        for key, values in pos.items():
                            for value in values:
                                print((key, value[1]), end='\n')
                        print()

                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            # dupa iesirea din while sigur am valida coloana
            # deci pot plasa simbolul pe "tabla de joc"
            poz_veche = (linie_veche, coloana_veche)
            numar_mutari_JMIN += 1  # facem o mutare

            i = 0  # Luam in dirs directiile pe care le-a folosit alg sa ajunga la poz noua
            dirs = pos[(linie, coloana)][0]
            while pos[(linie, coloana)][i][1] != poz_veche:
                i += 1
                dirs = pos[(linie, coloana)][i]

            if stare_curenta.tabla_joc.matr[linie_veche][coloana_veche] == Joc.JMIN:
                move(stare_curenta.tabla_joc.matr,
                     (linie, coloana), dirs, Joc.JMIN)
            else:
                move(stare_curenta.tabla_joc.matr,
                     (linie, coloana), dirs, Joc.JMIN.upper())

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # Scor
            stare_curenta.tabla_joc.print_scor()

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa - t_inainte) + " milisecunde.")

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)

            if afis_daca_final(stare_curenta, Joc.JMAX):
                break

            numar_mutari_JMAX += 1  # facem o mutare

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # Scor
            stare_curenta.tabla_joc.print_scor()

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa - t_inainte) + " milisecunde.")

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

    # Afisam numarul de mutari
    if Joc.JMAX == Joc.SIMBOLURI_JOC[0]:
        print(
            f"Numar mutari joc: pentru {Joc.SIMBOLURI_JOC[0]} = {numar_mutari_JMAX}, iar pentru {Joc.SIMBOLURI_JOC[1]} = {numar_mutari_JMIN}")
    else:
        print(
            f"Numar mutari joc: pentru {Joc.SIMBOLURI_JOC[0]} = {numar_mutari_JMIN}, iar pentru {Joc.SIMBOLURI_JOC[1]} = {numar_mutari_JMAX}")

    # preiau timpul in milisecunde de dupa joc
    t_dupa_joc = int(round(time.time() * 1000))
    print("Jocul a durat " +
          str(t_dupa_joc - t_iceputul_jocului) + " milisecunde.")


if __name__ == "__main__":
    main()

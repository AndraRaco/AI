import time
import copy


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 7
    NR_LINII = 6
    NR_CONNECT = 4  # cu cate simboluri adiacente se castiga
    SIMBOLURI_JUC = ['X', '0']  # ['G', 'R'] sau ['X', '0']
    JMIN = None  # 'R'
    JMAX = None  # 'G'
    GOL = '.'

    def __init__(self, tabla=None, ultim_poz=None):
        # self.matr = tabla or [Joc.GOL]*(Joc.NR_COLOANE * Joc.NR_LINII)

        self.matr = tabla or [[self.GOL for j in range(
            self.NR_COLOANE)] for i in range(self.NR_LINII)]
        # lista cu ultimile pozitii ocupate pe ficare coloana
        self.ultim_poz = ultim_poz or ([self.NR_LINII-1] * self.NR_COLOANE)

    # def __str__(self):
    #     return '\n'.join([' | '.join([str(u) for u in row]) for row in self.matr])

    def final(self):
        # returnam simbolul jucatorului castigator daca are 4 piese adiacente
        #	pe linie, coloana, diagonala \ sau diagonala /
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat jocul
        rez = False
        matrice = self.matr
        str_max = self.JMAX * self.NR_CONNECT
        str_min = self.JMIN * self.NR_CONNECT

        # verificam linii
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE - self.NR_CONNECT+1):
                if matrice[i][j: j + self.NR_CONNECT] == list(str_max):
                    return self.JMAX
                if matrice[i][j: j + self.NR_CONNECT] == list(str_min):
                    return self.JMIN

        # verificam coloane
        for i in range(self.NR_LINII - self.NR_CONNECT+1):
            for j in range(self.NR_COLOANE):
                str = ""
                for k in range(self.NR_CONNECT):
                    str += matrice[i + k][j]
                if str == str_max:
                    return self.JMAX
                if str == str_min:
                    return self.JMIN

        # verificam diagonale \
        for i in range(self.NR_LINII - self.NR_CONNECT+1):
            for j in range(self.NR_COLOANE - self.NR_CONNECT+1):
                str = ""
                for k in range(self.NR_CONNECT):
                    str += matrice[i + k][j+k]
                if str == str_max:
                    return self.JMAX
                if str == str_min:
                    return self.JMIN

        # verificam diagonale /
        for i in range(self.NR_LINII - self.NR_CONNECT+1):
            for j in reversed(range(self.NR_COLOANE - self.NR_CONNECT, self.NR_COLOANE)):
                str = ""
                for k in range(self.NR_CONNECT):
                    str += matrice[i + k][j-k]
                if str == str_max:
                    return self.JMAX
                if str == str_min:
                    return self.JMIN

        Set = []
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                Set.append(matrice[i][j])
        if rez == False and Joc.GOL not in Set:
            return 'remiza'
        else:
            return False

    def mutari(self, jucator_opus):
        l_mutari = []

        # TO DO..........
        # folosim:
        # matr_tabla_noua = list(self.matr)
        # .... "jucator_opus" (parametrul functiei) adauga o mutare in "matr_tabla_noua"
        # l_mutari.append(Joc(matr_tabla_noua))

        # Putem aduga piese doar langa cele deja puse, le dram drumu de sus pana jos
        # Deci verificam ultima pozitie ocupa de jos in sus pe fiecare coloana

        for j in reversed(range(self.NR_COLOANE)):
            if self.ultim_poz[j] == -1:
                continue
            else:
                i = self.ultim_poz[j]
                tabla_noua = copy.deepcopy(self.matr)
                tabla_noua[i][j] = jucator_opus
                ultim_poz_nou = copy.deepcopy(self.ultim_poz)
                ultim_poz_nou[j] -= 1
                l_mutari.append(Joc(tabla_noua, ultim_poz_nou))

        return l_mutari

    def nr_intervale_deschise(self, jucator):
        # un interval de 4 pozitii adiacente (pe linie, coloana, diag \ sau diag /)
        # este deschis pt "jucator" daca nu contine "joc_opus"

        juc_opus = Joc.JMIN if jucator == Joc.JMAX else Joc.JMAX
        rez = 0
        matrice = self.matr

        # linii
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE - self.NR_CONNECT+1):
                Set = []
                for k in range(self.NR_CONNECT):
                    Set.append(matrice[i][j + k])
                Set = set(Set)
                if Set <= {Joc.GOL, jucator}:  # incluziune de seturi
                    rez += 1

        # coloane
        for i in range(self.NR_LINII - self.NR_CONNECT+1):
            for j in range(self.NR_COLOANE):
                Set = []
                for k in range(self.NR_CONNECT):
                    Set.append(matrice[i + k][j])
                Set = set(Set)
                if Set <= {Joc.GOL, jucator}:  # incluziune de seturi
                    rez += 1

        # diagonale \
        for i in range(self.NR_LINII - self.NR_CONNECT+1):
            for j in range(self.NR_COLOANE - self.NR_CONNECT+1):
                Set = []
                for k in range(self.NR_CONNECT):
                    Set.append(matrice[i + k][j+k])
                Set = set(Set)
                if Set <= {Joc.GOL, jucator}:  # incluziune de seturi
                    rez += 1

        # diagonale /
        for i in range(self.NR_LINII - self.NR_CONNECT+1):
            for j in reversed(range(self.NR_COLOANE - self.NR_CONNECT, self.NR_COLOANE)):
                Set = []
                for k in range(self.NR_CONNECT):
                    Set.append(matrice[i + k][j-k])
                Set = set(Set)
                if Set <= {Joc.GOL, jucator}:  # incluziune de seturi
                    rez += 1

        return rez

    def fct_euristica(self):
        # TO DO: alte variante de euristici? .....

        # intervale_deschisa(juc) = cate intervale de 4 pozitii
        # (pe linii, coloane, diagonale) nu contin juc_opus
        return self.nr_intervale_deschise(Joc.JMAX) - self.nr_intervale_deschise(Joc.JMIN)

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (999+adancime)
        elif t_final == Joc.JMIN:
            return (-999-adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()

    def __str__(self):
        sir = ''
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + '   '
        sir += '\n'

        sir += '\n'.join([' | '.join([str(u) for u in row])
                          for row in self.matr])
        sir += '\n'
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

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent: "+self.j_curent+")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):

    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
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
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if(alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if(beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    # ?? TO DO:
    # de adagat parametru "pozitie", ca sa nu verifice mereu toata tabla,
    # ci doar linia, coloana, 2 diagonale pt elementul nou, de pe "pozitie"

    final = stare_curenta.tabla_joc.final()
    if(final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat "+final)

        return True

    return False


def main():
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
        n = input("Adancime maxima a arborelui: ")
        if n.isdigit():
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(
            input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2))).upper()
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
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
        tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    coloana = int(input("coloana = "))

                    # TO DO......
                    # de verificat daca "coloana" este in intervalul corect,
                    # apoi de gasit pe ce "linie" este cea mai de jos
                    # casuta goala de pe acea "coloana"

                    if coloana in range(0, stare_curenta.tabla_joc.NR_COLOANE):
                        linie = stare_curenta.tabla_joc.ultim_poz[coloana]

                        if linie == -1:
                            print("Toata coloana este ocupata.")
                        else:
                            raspuns_valid = True
                    else:
                        print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(
                            Joc.NR_COLOANE - 1))

                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            # dupa iesirea din while sigur am valida coloana
            # deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
            stare_curenta.tabla_joc.ultim_poz[coloana] -= 1

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":

    main()

    # joc = [
    #     ['.', '.', '.', '0', '.', '.', '.'],
    #     ['.', 'X', '.', '0', '.', '.', '.'],
    #     ['.', 'X', 'X', '0', '.', '.', '.'],
    #     ['.', '0', '0', 'X', '.', '.', '.'],
    #     ['.', 'X', 'X', '0', 'X', '.', '.'],
    #     ['0', 'X', 'X', 'X', '0', '.', '0'],
    # ]
    # ultim_poz = [4, 0, 1, -1, 3, 5, 4]
    # joc = Joc(joc, ultim_poz)
    # joc.JMAX = '0'
    # joc.JMIN = 'X'
    # final = joc.final()
    # print(final)

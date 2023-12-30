import pyodbc as odbccon

class vyhledavejVTabulkach:

    def __init__(self):

        self.vytvorCeleIfc(79107)


    def vytvorCeleIfc(self, hashMax):

        conn = self.pripojSeKDB()
        seznamIfc = []

        for i in range(1, hashMax):

            ifc = vratIfcRadek(conn, i)
            ifcRadek = ifc.getIfcRadek()

            if(ifcRadek != ''):
                seznamIfc.append(ifcRadek)

        print()


    def pripojSeKDB(self):
        conn = odbccon.connect("DRIVER={SQL Server Native Client 11.0};"
                               "Server=DESKTOP-U6S885I\SQLEXPRESS;"
                               "Database=HumanResources;"
                               "Trusted_Connection=yes;")

        return (conn)


class vratIfcRadek:

    def __init__(self, conn, indexHash):

        ifcRadekPotomci = self.ziskejIfcRadek(conn, indexHash)

        try:
            self.ifcRadek = ifcRadekPotomci[0]
            self.potomci = ifcRadekPotomci[1]
        except:
            self.ifcRadek = None
            self.potomci = []

        print()


    def getIfcRadek(self):
        return(self.ifcRadek)


    def getIfcPotomci(self):
        return(self.potomci)


    def ziskejIfcRadek(self, conn, indexHash):


        seznamRadkuTabulka = self.ziskejSeznamRadkuTabulky(conn, indexHash)
        seznamKandidatu = self.ziskejSeznamKandidatuTabulek(seznamRadkuTabulka)
        ifcRadekPotomci = self.vratIfcRadekDleHash(indexHash, conn, seznamKandidatu)

        return(ifcRadekPotomci)


    def ziskejSeznamKandidatuTabulek(self, seznamRadkuTabulka):

        seznamKandidatu = []

        for i in range(0, len(seznamRadkuTabulka)):
            radek = seznamRadkuTabulka[i]
            tabulkaKandidat = radek[3]
            tabulkaKandidat = tabulkaKandidat.replace('\'', '')
            tabulkaKandidat = tabulkaKandidat.replace(')', '')
            tabulkaKandidat = tabulkaKandidat.strip()

            seznamKandidatu.append(tabulkaKandidat)

        return(seznamKandidatu)


    def ziskejSeznamRadkuTabulky(self, conn, indexHash):

        if(indexHash == 'missing data in database'):
            tabulka = []

        else:
            seznamKandidatuSQL = 'SELECT * FROM overview WHERE (min <= ' + str(indexHash) + ') AND (max >= ' + str(indexHash) + ') ORDER BY rozdil;'

            cursor = conn.cursor()
            cursor.execute(seznamKandidatuSQL)

            seznamRadkuTabulka = []

            for row in cursor:
                try:
                    seznamRadkuTabulka.append(str(row))
                except:
                    break

            tabulka = self.prevedTabSQLnaTAb(seznamRadkuTabulka)

        return(tabulka)


    def prevedTabSQLnaTAb(self, tabSQL):

        tabulka = []

        for i in range(0, len(tabSQL)):
            radek = tabSQL[i]
            radekSpl = radek.split(',')

            tabulka.append(radekSpl)

        return (tabulka)






    def vratIfcRadekDleHash(self, hash, conn, seznamTabulek):

        ifcRadekPotomci = []

        for i in range(0, len(seznamTabulek)):

            nazevTabulky = seznamTabulek[i]
            dotaz = 'SELECT *  FROM ' + nazevTabulky + ' WHERE hash_Id = \'#'+ str(hash) +'\';'

            cursor = conn.cursor()
            cursor.execute(dotaz)

            for row in cursor:
                ifcRadekPotomci = self.vratRadekIfc(row, nazevTabulky, conn)
                break

        return(ifcRadekPotomci)


    def vratRadekIfc(self, row, nazevTabulky, conn):

        hashZavorka = self.vratObsahZavorkyIfcAHash(str(row))
        hash = hashZavorka[0]
        zavorka = hashZavorka[1]
        seznamPotomku = self.zeZavorkyVratSeznamPotomku(zavorka, nazevTabulky, conn)

        ifcRadek = hash + '= ' + nazevTabulky + zavorka

        ifcRadekPotomci = []
        ifcRadekPotomci.append(ifcRadek)
        ifcRadekPotomci.append(seznamPotomku)


        return(ifcRadekPotomci)


    def zeZavorkyVratSeznamPotomku(self, zavorka, nazevTabulky, conn):

        seznamPotomku = []

        zavorkaNew = zavorka.replace('(', '')
        zavorkaNew = zavorkaNew.replace(')', '')
        zavorkaNew = zavorkaNew.replace(' ', '')

        zavorkaSplit = zavorkaNew.split(',')

        for i in range(0, len(zavorkaSplit)):
            pol = zavorkaSplit[i]

            if(pol == '#93_4'):
                a = 5

            if(pol == ''):
                pol = 'missing data in database'
                seznamPotomku.append(pol)
            else:

                jednaSeOHash = self.detekujZdaSeJednaOHash(pol)

                if(jednaSeOHash == True):
                    polBezHash = pol.replace('#', '')
                    jednaSoOOdvozenyHash = self.detekujZdaSeJednaOOdvozenyHash(polBezHash)

                    # jelikož nemuzou byt za sebou 2 odvozene (2x vnorene) potomci
                    # nemuze se zacyklit, jinak by se zacyklil
                    if(jednaSoOOdvozenyHash == True):
                        ifcRadekPotomci = self.vratseznamPotomkuProOdvozenyHash(polBezHash, nazevTabulky, conn)
                        a = 5

                    polInt = int(polBezHash)
                    seznamPotomku.append(polInt)

        return(seznamPotomku)


    def vratseznamPotomkuProOdvozenyHash(self, odvozenyHash, nazevTabulky, conn):

        ifcRadekPotomci = []

        nazevOdvozeneTabulky = '_' + nazevTabulky
        podminkaWhere = 'hash_Id = \'' + odvozenyHash + '\''

        dotaz = 'SELECT * FROM ' + nazevOdvozeneTabulky + ' WHERE ' + podminkaWhere + ';'

        cursor = conn.cursor()
        cursor.execute(dotaz)

        for row in cursor:
            ifcRadekPotomci = self.vratRadekIfc(row, nazevTabulky)
            break

        return(ifcRadekPotomci)


    def detekujZdaSeJednaOHash(self, radek):

        prvniZnak = radek[0]

        jednaSeOHash = False

        if(prvniZnak == '#'):
            radekBezHash = radek.replace('#', '')
            try:
                hashIndex = int(radekBezHash)
                jednaSeOHash = True
            except:
                jednaSeOHash = False

        return(jednaSeOHash)


    def detekujZdaSeJednaOOdvozenyHash(self, polBezHash):

        polBezHashSpl = polBezHash.split('_')

        if(len(polBezHashSpl) == 2):
            jednaSoOOdvozenyHash = True
        else:
            jednaSoOOdvozenyHash = False

        return(jednaSoOOdvozenyHash)



    def vratObsahZavorkyIfcAHash(self, row):

        rowSpl = row.split(',')
        hash = rowSpl[0]
        hash = hash.replace('\'' ,'')
        hash = hash.replace('(', '')
        zavorka = '('

        for i in range(1, len(rowSpl)):
            pol = rowSpl[i]
            pol = pol.replace('\'' ,'')
            pol = pol.replace(')', '')

            zavorka = zavorka + pol

            if(i < len(rowSpl) - 1):
                zavorka = zavorka + ', '
            else:
                zavorka = zavorka + ')'

        hashZavorka = []
        hashZavorka.append(hash)
        hashZavorka.append(zavorka)

        return(hashZavorka)
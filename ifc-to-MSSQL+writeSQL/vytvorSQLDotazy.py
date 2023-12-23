

class vytvorTabulky:

    def __init__(self, dataVsechTabulek):

        dataVsechTabulekJakoTab = self.vratDataVsechTabulekJakoTab(dataVsechTabulek)
        nazvyTabulek = self.vratPole1DDleIndexu(dataVsechTabulek, 0)
        nazvyTabulek = self.opravNazvyTabulek(nazvyTabulek)
        pocetSloupcuArr = self.vratPoleSPoctemSloupcu(dataVsechTabulekJakoTab)

        nazvySloupcuVsechTabulek = self.vytvorVsechnyNazvySloupcu(pocetSloupcuArr)

        self.dotazyCreateTable = self.vytvorVsechnyDotazyCreateTable(nazvyTabulek, nazvySloupcuVsechTabulek)
        self.dotazyInsertInto = self.vytvorDotazyInsertInto(nazvyTabulek, nazvySloupcuVsechTabulek, dataVsechTabulekJakoTab)
        self.dotazyDropTable = self.vytvorDotazyDropTable(nazvyTabulek)


    def getDotazyCreateTable(self):
        return(self.dotazyCreateTable)


    def getDotazyInsertInto(self):
        return(self.dotazyInsertInto)


    def getDotazyDropTable(self):
        return (self.dotazyDropTable)



    def vytvorDotazyDropTable(self, nazvyTabulek):

        sqlDropArr = []

        for i in range(0, len(nazvyTabulek)):
            nazevTabulky = nazvyTabulek[i]

            if(nazevTabulky != ''):
                sqlDropTable = self.vytvorDotazDropTable(nazevTabulky)

                sqlDropArr.append(sqlDropTable)

        return(sqlDropArr)


    def vytvorDotazDropTable(self, nazevTabulky):

        sqlDropTable = 'DROP TABLE IF EXISTS ' + nazevTabulky
        return(sqlDropTable)


    def vytvorDotazyInsertInto(self, nazvyTabulek, nazvySloupcuVsechTabulek, dataVsechTabulekJakoTab):

        sqlIntoArr = []

        for i in range(0, len(nazvyTabulek)):
            nazevTabulky = nazvyTabulek[i]

            if(nazevTabulky != ''):
                nazvySloupcu = nazvySloupcuVsechTabulek[i]
                dataJedneTabulky = dataVsechTabulekJakoTab[i]

                sqlInsertInto = self.vytvorDotazInsertInto(nazevTabulky, nazvySloupcu, dataJedneTabulky)
                sqlIntoArr.append(sqlInsertInto)

        return(sqlIntoArr)


    def vytvorDotazInsertInto(self, nazevTabulky, nazvySloupcu, dataJedneTabulky):

        obsahZavorkySloupce = self.vratObsahZavorky(nazvySloupcu, False)
        obsahZavorkyData = self.vratObsahZavorky(dataJedneTabulky[0], True)
        sqlInsertInto = 'INSERT INTO ' + nazevTabulky + ' ' + obsahZavorkySloupce + ' VALUES ' + obsahZavorkyData

        return(sqlInsertInto)


    def vratObsahZavorky(self, nazvySloupcu, uvozovky):

        obsahZavorky = '('

        for i in range(0, len(nazvySloupcu)):
            nazevSloupce = nazvySloupcu[i]
            if(uvozovky == True):
                nazevSloupce = '\'' + str(nazevSloupce) + '\''

            promennaJePrazdna = self.detekujZdaJePromennaPrazdna(nazevSloupce)

            if(promennaJePrazdna == False):
                nazevSloupce = nazevSloupce.replace('\'\'', '\'')

            nazevSloupce = nazevSloupce.replace('\';\'', ';\'')


            obsahZavorky = obsahZavorky + nazevSloupce

            if (i < len(nazvySloupcu) - 1):
                obsahZavorky = obsahZavorky + ', '
            else:
                obsahZavorky = obsahZavorky + ')'

        return(obsahZavorky)


    def detekujZdaJePromennaPrazdna(self, promena):

        promennaTrim = promena.replace('\'', '')
        promennaTrim = promennaTrim.strip()
        if(promennaTrim == ''):
            promennaJePrazdna = True
        else:
            promennaJePrazdna = False

        return(promennaJePrazdna)


    def vytvorVsechnyNazvySloupcu(self, pocetSloupcuArr):

        nazvySloupcuVsechTabulek = []

        for i in range(0, len(pocetSloupcuArr)):
            pocetSloupcu = pocetSloupcuArr[i]
            nazvySloupcuTabulky = self.vytvorNazvySloupcuProJednuTabulku(pocetSloupcu)

            nazvySloupcuVsechTabulek.append(nazvySloupcuTabulky)

        return(nazvySloupcuVsechTabulek)


    def vytvorNazvySloupcuProJednuTabulku(self, pocetSloupcu):

        nazvySloupcuTabulky = []

        for i in range(0, pocetSloupcu):
            nazevSloupce = 'col_' + str(i + 1)
            nazvySloupcuTabulky.append(nazevSloupce)

        return(nazvySloupcuTabulky)


    def vytvorVsechnyDotazyCreateTable(self, nazvyTabulek, nazvySloupcuVsechTabulek):

        dotazyCreateTable = []

        for i in range(0, len(nazvyTabulek)):
            nazevTabulky = nazvyTabulek[i]

            if(nazevTabulky != ''):
                nazvySloupcu = nazvySloupcuVsechTabulek[i]

                dotazCreateTable = self.vytvorDotazCreateTable(nazevTabulky, nazvySloupcu)
                dotazyCreateTable.append(dotazCreateTable)

        return(dotazyCreateTable)


    def vytvorDotazCreateTable(self, nazevTab, nazvySloupcu):

        obsahZavorky = 'CREATE TABLE ' + nazevTab + ' ('

        for i in range(0, len(nazvySloupcu)):
            nazevSloupce = nazvySloupcu[i]
            nazevSloupceStr = '"' + nazevSloupce + '"' + ' varchar(255)'

            obsahZavorky = obsahZavorky + nazevSloupceStr

            if(i < len(nazvySloupcu)-1):
                obsahZavorky = obsahZavorky + ', '
            else:
                obsahZavorky = obsahZavorky + ')'

        return(obsahZavorky)


    def opravNazvyTabulek(self, nazvyTabulek):

        for i in range(0, len(nazvyTabulek)):
            nazevTabulky = nazvyTabulek[i]
            if(nazevTabulky == 'HEADER;FILE_DESCRIPTION'):
                nazevTabulky = 'FILE_DESCRIPTION'
                nazvyTabulek[i] = nazevTabulky

        return(nazvyTabulek)


    def vratPoleSPoctemSloupcu(self, dataVsechTabulekJakoTab):

        pocetSloupcuArr = []

        for i in range(0, len(dataVsechTabulekJakoTab)):

            radekTab = dataVsechTabulekJakoTab[i]
            pocetSloupcu = self.vratPocetSloupcuProJedenRadek(radekTab)

            pocetSloupcuArr.append(pocetSloupcu)

        return(pocetSloupcuArr)


    def vratPocetSloupcuProJedenRadek(self, radekTab):

        try:
            radekTabData = radekTab[0]
            pocetSloupcu = len(radekTabData)
        except:
            pocetSloupcu = -1

        return(pocetSloupcu)


    def vratDataVsechTabulekJakoTab(self, dataVsechTabulek):

        dataVsechTabulekJakoTab = []

        for i in range(0, len(dataVsechTabulek)):
            dataJedneTabulky = dataVsechTabulek[i]
            vsechnySloupceRadkuTabulky = self.vratSloupceProVsechnyRadky(dataJedneTabulky)

            dataVsechTabulekJakoTab.append(vsechnySloupceRadkuTabulky)

        return(dataVsechTabulekJakoTab)


    def vratSloupceProVsechnyRadky(self, dataJedneTabulky):

        vsechnySloupceRadkuTabulky = []

        for i in range(0, len(dataJedneTabulky[1])):

            radekTabulkyHashData = dataJedneTabulky[1][i]

            idHash = radekTabulkyHashData[0]
            radekTabulky = radekTabulkyHashData[1]

            radekSpl = self.rozdelRadekDoSloupcu(radekTabulky)
            radekSplHash = []

            radekSplHash.append(idHash)
            radekSplHash = radekSplHash + radekSpl

            vsechnySloupceRadkuTabulky.append(radekSplHash)

        return(vsechnySloupceRadkuTabulky)


    def rozdelRadekDoSloupcu(self, radek):

        try:
            radekSpl = radek.split(',')
        except:
            radekSpl = []

        return(radekSpl)


    def vratPole1DDleIndexu(self, pole2D, index):

        pole1D = []

        for i in range(0, len(pole2D)):

            radekPole = pole2D[i]
            try:
                hodnota = radekPole[index]
            except:
                hodnota = ''

            pole1D.append(hodnota)

        return(pole1D)




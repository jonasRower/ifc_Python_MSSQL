import vlozSQLdotazDoDB

class dataDavky:

    def __init__(self, ifcClasses, ifcClass, poleHashId, parametersArr):

        if(ifcClass != ''):

            if(ifcClass == '_IFCPOLYLOOP'):
                a = 5


            poleIndexu = self.ziskejPoleVsechIndexu(ifcClasses, ifcClass)
            rozdeleneRadkyTab = self.vratVsechnyRozdeleneRadkyDleTabulky(poleHashId, parametersArr, poleIndexu)
            dataTypeTypSloupceAll = self.urciDatoveTypyTabulky(rozdeleneRadkyTab)

            # opravi o prazdne polozky
            rozdeleneRadkyTab = self.podleDatovychTypuRozsirRadkyOPrazdnePolozky(dataTypeTypSloupceAll, rozdeleneRadkyTab)


            if (ifcClass == 'HEADER;FILE_DESCRIPTION'):
                nazevTabulky = 'FILE_DESCRIPTION'
            else:
                nazevTabulky = ifcClass


            #############################
            # dotazy pro jednu davku
            #############################

            # dropne tabulku, pokud existuje
            vlozSQLdotazDoDB.SQLDropTable(nazevTabulky)

            # vytvori tabulku
            vlozSQLdotazDoDB.SQLCreateTable(nazevTabulky, dataTypeTypSloupceAll)

            # vlozi data tabulky
            vlozSQLdotazDoDB.SQLInsertInto(nazevTabulky, dataTypeTypSloupceAll, rozdeleneRadkyTab)


            # ziska data k vraceni z tridy
            self.hashIdProJednuTabulku = self.seskupHashIdDoJednohoPole(rozdeleneRadkyTab)

            if(nazevTabulky == '_IFCPLANEANGLEMEASURE'):
                a = 5

        else:
            self.hashIdProJednuTabulku = [-1]


    def getHashIdProJednuTabulku(self):
        return(self.hashIdProJednuTabulku)


    # seskupuje datr, aby je mohl vratit nazpet z tridy
    # aby bylo mozne sestavit tabulku overview
    def seskupHashIdDoJednohoPole(self, rozdeleneRadkyTab):

        hashIdProJednuTabulku = []

        for i in range(0, len(rozdeleneRadkyTab)):

            hashId = rozdeleneRadkyTab[i][0]
            hashIdProJednuTabulku.append(hashId)

        return(hashIdProJednuTabulku)


    def podleDatovychTypuRozsirRadkyOPrazdnePolozky(self, dataTypeTypSloupceAll, rozdeleneRadkyTab):

        pocetSloupcuCelkem = len(dataTypeTypSloupceAll)
        radkyNew = []

        for i in range(0, len(rozdeleneRadkyTab)):
            radek = rozdeleneRadkyTab[i]
            radekNew = self.rozsirRadekOPrazdnePolozky(radek, pocetSloupcuCelkem)
            radkyNew.append(radekNew)

        return(radkyNew)


    def rozsirRadekOPrazdnePolozky(self, radek, pocetPolozekCelkem):

        pocetPolozekRadku = len(radek)

        for i in range(pocetPolozekRadku, pocetPolozekCelkem):
            radek.append('')

        return(radek)



    def urciDatoveTypyTabulky(self, rozdeleneRadkyTab):

        cislovaniHashCol = []

        pocetSloupcu = self.vratPocetSloupcu(rozdeleneRadkyTab)
        dataTypeTypSloupceAll = []


        for i in range(0, pocetSloupcu):
            dataJednohoSloupce = self.vratDataCelehoSloupce(rozdeleneRadkyTab, i)
            datovyTypSloupce = self.urciDatovyTypSloupce(dataJednohoSloupce)

            if(i == 0):
                refIdRefHashCol = 'hash_Id'
            else:
                jednaSeOHash = self.detekujZdaSeJednaOHashRef(dataJednohoSloupce)
                cislovaniHashCol = self.vratCislovaniHashCol(cislovaniHashCol, jednaSeOHash)

                if(jednaSeOHash == True):
                    refIdRefHashCol = 'hash_Ref'
                    cislovani = cislovaniHashCol[0]
                else:
                    refIdRefHashCol = 'col'
                    cislovani = cislovaniHashCol[1]

                refIdRefHashCol = refIdRefHashCol + '_' + str(cislovani)

            dataTypeTypSloupce = []
            dataTypeTypSloupce.append(datovyTypSloupce)
            dataTypeTypSloupce.append(refIdRefHashCol)

            dataTypeTypSloupceAll.append(dataTypeTypSloupce)

        return(dataTypeTypSloupceAll)


    def vratCislovaniHashCol(self, cislovaniHashCol, jednaSeOHash):

        if(len(cislovaniHashCol) == 0):
            cislovaniHashCol.append(0)
            cislovaniHashCol.append(0)

        if(jednaSeOHash == True):
            cislovaniHashCol[0] = cislovaniHashCol[0] + 1
        else:
            cislovaniHashCol[1] = cislovaniHashCol[1] + 1

        return(cislovaniHashCol)


    def detekujZdaSeJednaOHashRef(self, dataJednohoSloupce):

        jednaSeOHash = True

        for i in range(0, len(dataJednohoSloupce)):
            hodnota = dataJednohoSloupce[i]

            if(hodnota == ''):
                jednaSeOHash = False
            else:
                jednaSeOHash = self.detekujZdaSeJednaOHash(hodnota)

            if(jednaSeOHash == False):
                break

        return(jednaSeOHash)



    def detekujZdaSeJednaOHash(self, hodnota):

        prvniZnak = hodnota[0]
        jednaSeOHash = False

        if(prvniZnak == '#'):
            hodnotaBezHash = hodnota[1:len(hodnota):1]
            try:
                intHodnotaBezHash = int(hodnotaBezHash)
                jednaSeOHash = True
            except:
                jednaSeOHash = False

        return(jednaSeOHash)


    def vratPocetSloupcu(self, rozdeleneRadkyTab):

        pocetSloupcuMax = 0

        for i in range(0, len(rozdeleneRadkyTab)):
            dataNaRadku = rozdeleneRadkyTab[i]
            pocetSloupcu = len(dataNaRadku)

            if(pocetSloupcu > pocetSloupcuMax):
                pocetSloupcuMax = pocetSloupcu

        return(pocetSloupcuMax)


    def urciDatovyTypSloupce(self, dataJednohoSloupce):

        for i in range(0, len(dataJednohoSloupce)):
            hodnota = dataJednohoSloupce[i]

            try:
                hodnotaInt = int(hodnota)
                datovyTyp = 'int'
            except:
                datovyTyp = 'varchar(255)'
                break

        return(datovyTyp)




    # seskupi data vsech radku tabulky, pro jeden sloupec, do pole
    def vratDataCelehoSloupce(self, rozdeleneRadkyTab, indexSloupce):

        dataJednohoSloupce = []

        for i in range(0, len(rozdeleneRadkyTab)):
            try:
                hodnota = rozdeleneRadkyTab[i][indexSloupce]
            except:
                hodnota = ''

            dataJednohoSloupce.append(hodnota)

        return(dataJednohoSloupce)


    # rozdeli data na hashId, hashRef, col
    def rozdelSloupceNaHashIdHashRefCol(self, rozdeleneRadkyTab):

        for i in range(0, len(rozdeleneRadkyTab)):
            dataJednohoRadkuTabulky = rozdeleneRadkyTab[i]



    #def vratDatoveTypySloupcu(self):
    #def zjistiuDatovyTypCelehoSloupce(self, dataCelehoSloupce):


    def ziskejPoleVsechIndexu(self, poleRadku, radek):

        poleIndexu = []

        for i in range(0, len(poleRadku)):

            try:
                ind = poleRadku.index(radek)
                poleIndexu.append(ind)

                poleRadku[ind] = ''

            except:
                break

        return(poleIndexu)


    def vratVsechnyRozdeleneRadkyDleTabulky(self, poleHashId, parametersArr, indexyRadku):

        rozdeleneRadkyTab = []

        for i in range(0, len(indexyRadku)):

            indexRadku = indexyRadku[i]
            hashId = poleHashId[indexRadku]
            parameters = parametersArr[indexRadku]
            poleParametru = self.vratPoleParametru(parameters, hashId)

            rozdeleneRadkyTab.append(poleParametru)

        return(rozdeleneRadkyTab)


    def vratPoleParametru(self, parameters, hashId):

        hashParametry = []
        hashParametry.append(hashId)

        try:
            poleParametru = parameters.split(',')
        except:
            poleParametru = []

        hashParametry = hashParametry + poleParametru

        return(hashParametry)


    def vratPocetSloupcuProJedenRadek(self, radekTab):

        try:
            radekTabData = radekTab[0]
            pocetSloupcu = len(radekTabData)
        except:
            pocetSloupcu = -1

        return(pocetSloupcu)







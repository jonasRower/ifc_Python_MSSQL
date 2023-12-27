# vytvori tabulku, ktera spojuje jednotlive hash s nazvy tabulek

import vlozSQLdotazDoDB

class tabulkaOverview:

    def __init__(self, ifcClassesUniq, hashIdProTabulkyAll):

        #############################
        # tabulku overview 1000 nepouzivam, tudiz kod je nakonec prestaven tak, aby se do overview1000 nezapisovalo
        #############################

        pocetSloupcuNaZalomeni = 1000

        poctySloupcuArr = self.vratPoleSPoctySloupcu(hashIdProTabulkyAll)
        polePolozek1000All = self.zalomRadkyDelsiNez1000(poctySloupcuArr, hashIdProTabulkyAll, ifcClassesUniq, pocetSloupcuNaZalomeni)
        radkyOverview1000 = self.sestavTabulku1000(polePolozek1000All)

        nazevTabHashAll = self.doplnNazvyTabulekKHashId(hashIdProTabulkyAll, ifcClassesUniq, polePolozek1000All)


        self.zapisujTabulkuDoDB('overview', nazevTabHashAll)
        #self.zapisujTabulkuDoDB('overview1000', radkyOverview1000)



    def zapisujTabulkuDoDB(self, nazevTabulky, radkyOverview):

        poctySloupcuArr = self.vratPoleSPoctySloupcu(radkyOverview)
        pocetSloupcuMax = max(poctySloupcuArr)

        radkyOverview = self.vratMinMaxHashAll(radkyOverview)
        #radkyOverview = self.doplnRadkyNaStejnyPocetSloupcu(radkyOverview, pocetSloupcuMax)
        nazvyADataTypes = self.vytvorNazvySloupcuADatTypy(pocetSloupcuMax)

        #############################
        # dotazy pro vytvoreni tabulky overview
        #############################

        # dropne tabulku, pokud existuje
        vlozSQLdotazDoDB.SQLDropTable(nazevTabulky)

        # vytvori tabulku
        vlozSQLdotazDoDB.SQLCreateTable(nazevTabulky, nazvyADataTypes)

        # vlozi data tabulky
        vlozSQLdotazDoDB.SQLInsertInto(nazevTabulky, nazvyADataTypes, radkyOverview)





    def sestavTabulku1000(self, polePolozek1000All):

        tabulka1000 = []

        for i in range(0, len(polePolozek1000All)):
            subTabulka1000 = polePolozek1000All[i]
            tabulka1000 = tabulka1000 + subTabulka1000

        return(tabulka1000)


    def vytvorNazvySloupcuADatTypy(self, poctySloupcuArr):

        nazevDataTypeRozdil = ['int', 'rozdil']
        nazevDataTypeMin = ['int', 'min']
        nazevDataTypeMax = ['int', 'max']
        nazevDataTypeIfcClass = ['varchar(255)', 'ifcClass']

        nazvyADataTypes = []
        nazvyADataTypes.append(nazevDataTypeRozdil)
        nazvyADataTypes.append(nazevDataTypeMin)
        nazvyADataTypes.append(nazevDataTypeMax)
        nazvyADataTypes.append(nazevDataTypeIfcClass)

        """
        for i in range(4, poctySloupcuArr):
            nazevCol = 'hash_Ref_' + str(i-3)
            nazevDataType = ['varchar(16)', nazevCol]
            nazvyADataTypes.append(nazevDataType)
        """

        return(nazvyADataTypes)



    def doplnNazvyTabulekKHashId(self, hashIdProTabulkyAll, nazvyTabulek, polePolozek1000All):

        nazevTabHashAll = []

        for i in range(0, len(nazvyTabulek)):
            nazevTabulky = nazvyTabulek[i].strip()
            dataDleNazvuTab1000 = self.vratDataZ1000All(polePolozek1000All, nazevTabulky)

            #if(dataDleNazvuTab1000[0] == -1):
            radekHash = hashIdProTabulkyAll[i]

            nazevTabHash = []
            nazevTabHash.append(nazevTabulky)
            nazevTabHash = nazevTabHash + radekHash

            nazevTabHashAll.append(nazevTabHash)

            print()

            #else:
            # zde jiz je nazev spojeny, maximalni pocet sloupcu je 1000
            #nazevTabHashAll.append([[-1]])

        return(nazevTabHashAll)



    def vratDataZ1000All(self, polePolozek1000All, nazevTabulkyExp):

        dataDleNazvuTab1000 = [-1]

        for i in range(0, len(polePolozek1000All)):
            nazevTabulky = polePolozek1000All[i][0][0]
            if(nazevTabulky == nazevTabulkyExp):
                dataDleNazvuTab1000 = polePolozek1000All[i]
                break

        return(dataDleNazvuTab1000)


    def zalomRadkyDelsiNez1000(self, poctySloupcuArr, hashIdProTabulkyAll, nazvyTabulek, pocetSloupcuNaZalomeni):

        polePolozek1000All = []

        for i in range(0, len(poctySloupcuArr)):
            pocetSloupcu = poctySloupcuArr[i]
            if(pocetSloupcu > pocetSloupcuNaZalomeni):
                radek = hashIdProTabulkyAll[i]
                nazevTabulky = nazvyTabulek[i].strip()

                polePolozek1000 = self.zalomRadek(radek, nazevTabulky, pocetSloupcuNaZalomeni)

                polePolozek1000All.append(polePolozek1000)


        return(polePolozek1000All)


    def zalomRadek(self, radek, nazevTabulky, pocetSloupcuNaZalomeni):

        polePolozek1000 = []
        polePolozek1000All = []
        i_1000 = -1

        polePolozek1000.append(nazevTabulky)

        for i in range(0, len(radek)):
            i_1000 = i_1000 + 1
            polozka = radek[i]
            polePolozek1000.append(polozka)

            if(i_1000 == pocetSloupcuNaZalomeni):
                polePolozek1000All.append(polePolozek1000)
                polePolozek1000 = []
                polePolozek1000.append(nazevTabulky)
                i_1000 = -1

        polePolozek1000All.append(polePolozek1000)

        return(polePolozek1000All)


    def doplnRadkyNaStejnyPocetSloupcu(self, radkyOverview, pocetSloupcuMax):

        radkyOverviewNew = []

        for i in range(0, len(radkyOverview)):
            radekOverview = radkyOverview[i]

            if(radekOverview[0] != -1):
                pocetSloupcuRadek = len(radekOverview)

                doplnPocetSloupcu = pocetSloupcuMax - pocetSloupcuRadek
                radekOverview = self.doplnRadekODanyPocetSloupcu(radekOverview, doplnPocetSloupcu)

                radkyOverviewNew.append(radekOverview)

        return(radkyOverviewNew)


    def doplnRadekODanyPocetSloupcu(self, radekOverview, doplnPocetSloupcu):

        for i in range(0, doplnPocetSloupcu):
            radekOverview.append('')

        return(radekOverview)


    def vratPoleSPoctySloupcu(self, radkyOverview):

        poctySloupcuArr = []

        for i in range(0, len(radkyOverview)):
            radek = radkyOverview[i]
            pocetSloupcu = len(radek)

            poctySloupcuArr.append(pocetSloupcu)

        return(poctySloupcuArr)


    def vratMinMaxHashAll(self, nazevTabHashAll):

        radkyOverview = []

        for i in range(0, len(nazevTabHashAll)):
            nazevTabHashAllRadek = nazevTabHashAll[i]

            if(len(nazevTabHashAllRadek) > 1):
                if(nazevTabHashAllRadek[1] != -1):

                    hashMinMaxInt = self.vratMinMaxRadek(nazevTabHashAllRadek)
                    radekOverview = hashMinMaxInt
                    radekOverview = radekOverview + [nazevTabHashAllRadek[0]]

                    radkyOverview.append(radekOverview)


        return(radkyOverview)


    def vratMinMaxRadek(self, hashIdProTabulkyRadek):


        hashMinMaxInt = []

        hashMin = hashIdProTabulkyRadek[1]
        hashMax = hashIdProTabulkyRadek[len(hashIdProTabulkyRadek)-1]

        idMin = self.vratIdInt(hashMin)
        idMax = self.vratIdInt(hashMax)

        rozdil = idMax - idMin

        hashMinMaxInt.append(rozdil)
        hashMinMaxInt.append(idMin)
        hashMinMaxInt.append(idMax)

        return(hashMinMaxInt)



        """

        self.vytvorTabOverView(ifcClassesUniq, hashIdProTabulkyAll)
        

    def vytvorTabOverView(self, ifcClasses, poleHashId):

        dataTypeSloupce = [['varchar(255)', 'hash_Id'], ['varchar(255)', 'col_1']]
        nazevTabulky = 'overview'
        dataTabulky = self.vytvorDataTabulky(ifcClasses, poleHashId)


        #############################
        # dotazy pro vytvoreni tabulky overview
        #############################

        # dropne tabulku, pokud existuje
        vlozSQLdotazDoDB.SQLDropTable(nazevTabulky)

        # vytvori tabulku
        vlozSQLdotazDoDB.SQLCreateTable(nazevTabulky, dataTypeSloupce)

        # vlozi data tabulky
        vlozSQLdotazDoDB.SQLInsertInto(nazevTabulky, dataTypeSloupce, dataTabulky)
        """

    def vratIdInt(self, hashId):

        if(hashId == ''):
            idInt = -1
        else:
            id = hashId.replace('#', '')
            idInt = int(id)

        return(idInt)


    def vytvorDataTabulky(self, ifcClasses, poleHashId):

        dataTabulky = []

        for i in range(0, len(poleHashId)):

            hashId = poleHashId[i]
            nazevTabulky = ifcClasses[i].strip()

            hashIdNazevTabulky = []
            hashIdNazevTabulky.append(hashId)
            hashIdNazevTabulky.append(nazevTabulky)

            dataTabulky.append(hashIdNazevTabulky)

        return(dataTabulky)


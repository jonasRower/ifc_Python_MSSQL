import vyhledejDataDavky
import vytvorOverview
import copy
import odesilejDataDoDB

class vytvorTabulky:

    def __init__(self, poleRozdelenychRadku):

        poleHashId = self.vratPole1DDleIndexu(poleRozdelenychRadku, 0)
        poleClass = self.vratPole1DDleIndexu(poleRozdelenychRadku, 1)

        ifcClassesRadky = self.vratIfcClassParr(poleClass)
        ifcClasses = self.vratPole1DDleIndexu(ifcClassesRadky, 0)
        parametersArr = self.vratPole1DDleIndexu(ifcClassesRadky, 1)


        # ziska o desle odvozene sady dat
        parametersArrNew = self.odesilejOdvozeneSadyDat(ifcClasses, poleHashId, parametersArr)

        # odesli zakladni sadu dat
        self.odesliZakladniSaduDat(ifcClasses, poleHashId, parametersArrNew)



    # odesila sady dat
    def odesliZakladniSaduDat(self, ifcClasses, poleHashId, parametersArr):

        odesilejDataDoDB.sendDataToDB(ifcClasses, poleHashId, parametersArr)


    def odesilejOdvozeneSadyDat(self, ifcClasses, poleHashId, parametersArr):

        odvozeneSady = nahrazujParVirtId(parametersArr, ifcClasses, poleHashId)

        # ziska data getry
        parametersArr2D = odvozeneSady.getParametersArr2D()
        ifcClasses2D = odvozeneSady.getIfcClasses2D()
        poleHashId2D = odvozeneSady.getPoleHashId()
        parametersArrNew = odvozeneSady.getParametersArrNew()
        pocetSloupcuMax = odvozeneSady.getPocetSloupcuMax()

        self.prevedDataDoDBNa1DAll(poleHashId2D, ifcClasses2D, parametersArr2D, pocetSloupcuMax)

        return(parametersArrNew)


    def prevedDataDoDBNa1DAll(self, poleHashId2D, ifcClasses2D, parametersArr2D, pocetSloupcuMax):

        for i in range(0, pocetSloupcuMax-1):
            allData1Sloupec = self.prevedDataDoDBNa1D(poleHashId2D, ifcClasses2D, parametersArr2D, i)

            poleHashId = self.vratPole1DDleIndexu(allData1Sloupec, 0)
            ifcClasses = self.vratPole1DDleIndexu(allData1Sloupec, 1)
            parametersArr = self.vratPole1DDleIndexu(allData1Sloupec, 2)

            odesilejDataDoDB.sendDataToDB(ifcClasses, poleHashId, parametersArr)


    def prevedDataDoDBNa1D(self, poleHashId2D, ifcClasses2D, parametersArr2D, index):

        allData = []

        for i in range(0, len(ifcClasses2D)):

            try:
                hashId = poleHashId2D[i][index]
                ifcClass = ifcClasses2D[i][index]
                parameter = parametersArr2D[i][index]

                hashClassPar = []
                hashClassPar.append(hashId)
                hashClassPar.append(ifcClass)
                hashClassPar.append(parameter)

                allData.append(hashClassPar)

            except:
                pass

        return(allData)





    def vratIfcClassParr(self, poleClass):

        ifcClassesArr = []

        for i in range(0, len(poleClass)):

            radek = poleClass[i]
            radekObsahujeZavoku = self.detekujSubstr(radek, '(')

            if(radekObsahujeZavoku == True):
                indexZavorky = radek.index('(')
                x = slice(0, indexZavorky)
                ifcClass = radek[x]

                x = slice(indexZavorky, len(radek))
                obsahZavorky = radek[x]

                cistyObsahZavorky = self.vratCistyObsahZavorky(obsahZavorky)

            else:
                ifcClass = ''
                cistyObsahZavorky = []

            ifcClassPar = []

            ifcClassPar.append(ifcClass)
            ifcClassPar.append(cistyObsahZavorky)

            ifcClassesArr.append(ifcClassPar)

        return(ifcClassesArr)



    def vratCistyObsahZavorky(self, radek):

        prvniZnak = radek[0]
        posledniZnak = radek[-1]
        radekNew = radek

        if(prvniZnak == '('):
            radekNew = radekNew[1:len(radekNew):1]

        if (posledniZnak == ')'):
            radekNew = radekNew[0:len(radekNew)-1:1]


        cistyObsahZavorky = radekNew.replace('\n', '')

        return(cistyObsahZavorky)


    def vratPole1DDleIndexu(self, pole2D, index):

        pole1D = []

        for i in range(0, len(pole2D)):

            radekPole = pole2D[i]
            hodnota = radekPole[index]

            pole1D.append(hodnota)

        return(pole1D)


    def detekujSubstr(self, radek, subStr):

        try:
            ind = radek.index(subStr)
            radekObsahujeSubStr = True
        except:
            radekObsahujeSubStr = False

        return(radekObsahujeSubStr)



# nahrazuje prametry s fiktivnimi Id
# pro fiktivniId pak vytvari tabulku, samostatne
class nahrazujParVirtId:

    #potreba udelat tabulku spojujici nazvy tabulek s "_"

    def __init__(self, parametersArr, ifcClasses, poleHashId):

        prvniIndex = self.detekujPrvniPlatnyIfcClass(poleHashId)
        poleIndexuRadku = self.vratPoleIndexuRadkuSeZavorkami(parametersArr, prvniIndex)

        # redukuje jen na potrebne radky
        parametryDleIndexu = self.vratPoleRadkuDleIndexu(poleIndexuRadku, parametersArr)
        ifcClassesDleIndexu = self.vratPoleRadkuDleIndexu(poleIndexuRadku, ifcClasses)
        hashIdDleIndexu = self.vratPoleRadkuDleIndexu(poleIndexuRadku, poleHashId)

        # vrati pole s pocty zavorek na radcich
        pocetZavorekArr = self.vratPoleSPoctemZavorek(parametryDleIndexu)

        # ke vsem radkum priradi dvojice indexu zacatku a koncu zavorek, tam kde je vice sloupcu, tam je pole delsi
        indexyZavorekArr = self.vratZavorkyNaRadcich(parametryDleIndexu, pocetZavorekArr)

        # vrati indexy sloupcu - to prida k hashId aby vedel z jakeho sloupce tabulky je uvazovana zavorka
        indexSloupceAll = self.vratIndexySloupcuAll(indexyZavorekArr, parametryDleIndexu)

        # z parametru pred zavorkami vytvori nazvy tabulek,
        # tam kde parametr pred zavorkou neni, tam pouzije nazev tabulky aktualni
        nazvyTabulekAll = self.vratParPredZavorkamiAll(parametryDleIndexu, indexyZavorekArr, ifcClassesDleIndexu)

        # vrati obsahy vsech zavorek - tj. data ktera budou v tabulkach
        zavorkyAll = self.vratObsahyZavorek(parametryDleIndexu, indexyZavorekArr)

        # vrati hashId
        hashSloupecArr = self.vratHashId(hashIdDleIndexu, indexSloupceAll)

        # nahradi zavorky u radku s hash, tak aby se na ne spravne odkazoval v db
        parametryDleIndexuNew = self.nahradZavorkyParametruSHash(parametryDleIndexu, hashSloupecArr, zavorkyAll, nazvyTabulekAll)

        # vrati parametersArrNew tak aby mohl zapsat data do originalnich tabulek
        parametersArrNew = self.vytvorParametrsArrNew(parametersArr, parametryDleIndexuNew, poleIndexuRadku)
        print()

        # vrati data
        self.parametersArr2D = zavorkyAll
        self.ifcClasses2D = nazvyTabulekAll
        self.poleHashId = hashSloupecArr
        self.parametersArrNew = parametersArrNew

        self.pocetSloupcuMax = self.vratPocetSloupcu(pocetZavorekArr)


    def getParametersArr2D(self):
        return(self.parametersArr2D)

    def getIfcClasses2D(self):
        return(self.ifcClasses2D)

    def getPoleHashId(self):
        return(self.poleHashId)

    def getParametersArrNew(self):
        return (self.parametersArrNew)

    def getPocetSloupcuMax(self):
        return (self.pocetSloupcuMax)


    # aby mohl parametry predat nazpet
    def vytvorParametrsArrNew(self, parametersArr, parametryDleIndexu, poleIndexuRadku):

        parametersArrNew = []
        i1 = 0

        for i in range(0, len(parametersArr)):

            jeIndexVPoli = self.detekujSubstr(poleIndexuRadku, i)
            if(jeIndexVPoli == True):
                radek = parametryDleIndexu[i1]
                i1 = i1 + 1
            else:
                radek = parametersArr[i]

            parametersArrNew.append(radek)

        return(parametersArrNew)


    def vratPocetSloupcu(self, pocetZavorekArr):

        pocetSloupcuMax = 0

        for i in range(0, len(pocetZavorekArr)):
            pocetSloupcu = pocetZavorekArr[i]

            if(pocetSloupcu > pocetSloupcuMax):
                pocetSloupcuMax = pocetSloupcu

        return(pocetSloupcuMax)


    # nahradi zavorky na radcich novymi hash,
    # tak aby pri zapisu do DB se v jednotlivych bunkach zobrazoval odkaz hash
    def nahradZavorkyParametruSHash(self, parametryDleIndexu, hashSloupecArr, zavorkyAll, nazvyTabulekAll):

        parametryDleIndexuNew = []

        for i in range(0, len(parametryDleIndexu)):
            radek = parametryDleIndexu[i]
            nahradHash = hashSloupecArr[i]
            zavorkyRadek = zavorkyAll[i]
            nazevTabulky = nazvyTabulekAll[i]

            radek = self.nahrazujRadek(zavorkyRadek, nahradHash, radek, nazevTabulky)
            parametryDleIndexuNew.append(radek)

        return(parametryDleIndexuNew)


    def nahrazujRadek(self, zavorkyPuvodni, zavorkyNove, radek, nazevTabulkyRadek):

        for i in range(0, len(zavorkyPuvodni)):
            nazevTabulky = nazevTabulkyRadek[i]
            nazevTabulky = self.ziskejNazevTabulkyBezPodtrzitka(nazevTabulky)
            zavorkaOrig = '(' + zavorkyPuvodni[i] + ')'
            zavorkaNew = zavorkyNove[i]

            # zatim nekontroluji, zda zavorkaOrig jejedinecna, kdyby byla chyba, pak dodelat pres indexy zavorek
            radek = radek.replace(nazevTabulky, '')
            radek = radek.replace(zavorkaOrig, zavorkaNew)

        return(radek)


    def ziskejNazevTabulkyBezPodtrzitka(self, nazevTabulky):

        prvniZnak = nazevTabulky[0]
        if (prvniZnak == '_'):
            nazevTabulky = nazevTabulky[1:len(nazevTabulky):1]

        return(nazevTabulky)



    # hashId je doplneno o index sloupce tabulky
    def vratHashId(self, hashIdDleIndexu, indexSloupceAll):

        hashSloupecArr = []

        for i in range(0, len(hashIdDleIndexu)):

            hashId = hashIdDleIndexu[i]
            indexySloupcu = indexSloupceAll[i]

            hashSloupec = self.spojHashIndexSloupce(hashId, indexySloupcu)
            hashSloupecArr.append(hashSloupec)

        return(hashSloupecArr)


    def spojHashIndexSloupce(self, hashId, indexySloupcu):

        hashSloupecArr = []

        for i in range(0, len(indexySloupcu)):
            indexSloupce = indexySloupcu[i]
            hashSloupec = str(hashId) + '_' + str(indexSloupce)

            hashSloupecArr.append(hashSloupec)

        return(hashSloupecArr)


    # vrati obsahy zavorek, tak jak budou v databazi
    def vratObsahyZavorek(self, parametryDleIndexu, indexyZavorekArr):

        zavorkyAll = []

        for i in range(0, len(parametryDleIndexu)):
            radek = parametryDleIndexu[i]
            indexyZavorekRadek = indexyZavorekArr[i]

            zavorkyNaRadku = self.vratObsahyZavorekProRadek(indexyZavorekRadek, radek)
            zavorkyAll.append(zavorkyNaRadku)

        return(zavorkyAll)


    def vratObsahyZavorekProRadek(self, indexyZavorekRadek, radek):

        zavorkyNaRadku = []

        for i in range(0, len(indexyZavorekRadek)):
            zavOt = indexyZavorekRadek[i][0]
            zavZav = indexyZavorekRadek[i][1]

            x = slice(zavOt, zavZav)
            obsahZavorky = radek[x]
            zavorkyNaRadku.append(obsahZavorky)

        return(zavorkyNaRadku)


    def vratPoleRadkuDleIndexu(self, poleIndexuRadku, poleRadku):

        radkyDleIndexu = []

        for i in range(0, len(poleIndexuRadku)):
            indexRadku = poleIndexuRadku[i]
            radek = poleRadku[indexRadku]

            radkyDleIndexu.append(radek)

        return(radkyDleIndexu)


    def vratZavorkyNaRadcich(self, parametersArr, pocetZavorekArr):

        zavOtZavAllArr = []

        for i in range(0, len(parametersArr)):
            pocetZavorek = pocetZavorekArr[i]
            radek = parametersArr[i]
            zavOtZavAll = self.vratIndexOtAZavZav(radek, pocetZavorek)

            zavOtZavAllArr.append(zavOtZavAll)

        return(zavOtZavAllArr)


    def vratIndexySloupcuAll(self, indexyZavorekArr, parametersArr):

        indexSloupceAll = []

        for i in range(0, len(indexyZavorekArr)):
            zavOtZavAll = indexyZavorekArr[i]
            radek = parametersArr[i]
            mezilehleStringyAll = self.vratMezilehleStringy(zavOtZavAll, radek)
            indexSloupce = self.vratIndexySloupcu(mezilehleStringyAll)

            indexSloupceAll.append(indexSloupce)

        return(indexSloupceAll)


    def vratZavorkyNaRadcich2(self, parametersArr, poleIndexuRadku, pocetZavorekArr):

        zavorkyNaRadkuAll = []
        indexSloupceAll = []
        mezilehleStringyArr = []

        for i in range(0, len(poleIndexuRadku)):
            indexRadku = poleIndexuRadku[i]
            radek = parametersArr[indexRadku]
            pocetZavorek = pocetZavorekArr[i]

            zavOtZavAll = self.vratIndexOtAZavZav(radek, pocetZavorek)
            zavorkyNaRadku = self.vratVsechnyZavorkyNaRadku(radek, zavOtZavAll)
            mezilehleStringyAll = self.vratMezilehleStringy(zavOtZavAll, radek)

            indexSloupce = self.vratIndexySloupcu(mezilehleStringyAll)
            mezilehleStringyArr.append(mezilehleStringyAll)

            indexSloupceAll.append(indexSloupce)
            zavorkyNaRadkuAll.append(zavorkyNaRadku)

        zavorkyAIndexySloupcu = []
        zavorkyAIndexySloupcu.append(zavorkyNaRadkuAll)
        zavorkyAIndexySloupcu.append(indexSloupceAll)

        return(zavorkyAIndexySloupcu)


    #index sloupce tabulky spocita dle poctu carek
    def vratIndexySloupcu(self, mezilehleStringyAll):

        pocetCarekTot = 0
        indexSloupce = []

        for i in range(0, len(mezilehleStringyAll)):
            radek = mezilehleStringyAll[i]
            pocetCarek = radek.count(',')

            pocetCarekTot = pocetCarekTot + pocetCarek
            indexSloupce.append(pocetCarekTot)

        return(indexSloupce)



    def vratMezilehleStringy(self, zavOtZavAll, radek):

        strOt = 0
        mezilehleStringyAll = []

        for i in range(0, len(zavOtZavAll)):
            strZav = zavOtZavAll[i][0] - 1

            x = slice(strOt, strZav)
            mezilehlyString = radek[x]
            mezilehleStringyAll.append(mezilehlyString)

            strOt = zavOtZavAll[i][1] + 1

        return(mezilehleStringyAll)


    def vratIndexOtAZavZav(self, radek, pocetZavorekNaRadku):

        indexZavOt = 0
        indexZavZav = 0

        zavOtZavAll = []

        for i in range(0, pocetZavorekNaRadku):

            try:
                indexZavOt = radek.index('(', indexZavOt) + 1
                indexZavZav = radek.index(')', indexZavZav)

                zavOtZav = []
                zavOtZav.append(indexZavOt)
                zavOtZav.append(indexZavZav)

                zavOtZavAll.append(zavOtZav)

            except:
                pass

        return(zavOtZavAll)


    def vratVsechnyZavorkyNaRadku(self, radek, zavOtZavAll):

        zavorkyNaRadku = []

        for i in range(0, len(zavOtZavAll)):
            indexZavOt = zavOtZavAll[i][0]
            indexZavZav = zavOtZavAll[i][1]

            x = slice(indexZavOt, indexZavZav)
            obsahZavorky = radek[x]
            zavorkyNaRadku.append(obsahZavorky)

        return(zavorkyNaRadku)


    def vratPoleSPoctemZavorek(self, parametersArr):

        pocetZavorekArr = []

        for i in range(0, len(parametersArr)):
            radek = parametersArr[i]
            pocetZavorek = radek.count('(')

            pocetZavorekArr.append(pocetZavorek)

        return(pocetZavorekArr)


    def vratParPredZavorkamiAll(self, parametersArr, indexyZavorekArr, ifcClassesDleIndexu):

        parAll = []

        for i in range(0, len(parametersArr)):
            radek = parametersArr[i]
            indexyZavorekRadek = indexyZavorekArr[i]
            ifcClass = ifcClassesDleIndexu[i]

            parProRadek = self.vratParPredZavorkamiRadek(radek, indexyZavorekRadek, ifcClass)
            parAll.append(parProRadek)

        return(parAll)



    def vratParPredZavorkamiRadek(self, radek, indexyZavorekRadek, ifcClass):

        parProRadek = []

        for i in range(0, len(indexyZavorekRadek)):
            indexZavorky = indexyZavorekRadek[i][0] - 1

            x = slice(0, indexZavorky)
            stringPredZavorkou = radek[x]

            pouzitIfcClass = self.detekujZdaPouzitIfcClass(stringPredZavorkou)

            if (pouzitIfcClass == True):
                par = ifcClass.strip()
            else:
                strPredZavClear = self.ocistiStrPredZavorkou(stringPredZavorkou)
                par = strPredZavClear

            par = '_' + par
            parProRadek.append(par)

        return(parProRadek)


    def ocistiStrPredZavorkou(self, stringPredZavorkou):

        stringPredZavorkouSpl = stringPredZavorkou.split(',')
        strPredZavClear = stringPredZavorkouSpl[len(stringPredZavorkouSpl)-1]
        strPredZavClear = strPredZavClear.strip()

        return(strPredZavClear)


    #pokud je prazdny, nevo konci carkou, pak se pouzije ifcClass
    def detekujZdaPouzitIfcClass(self, stringPredZavorkou):

        if(stringPredZavorkou == ''):
            pouzitIfcClass = True
        else:
            posledniZnak = stringPredZavorkou[-1]
            if(posledniZnak == ','):
                pouzitIfcClass = True
            else:
                pouzitIfcClass = False

        return(pouzitIfcClass)


    def vratPoleIndexuRadkuSeZavorkami(self, parametersArr, prvniIndex):

        poleIndexuRadku = []

        for i in range(prvniIndex, len(parametersArr)):
            radek = parametersArr[i]
            radekObsahujeZavorku = self.detekujSubstr(radek, '(')

            if(radekObsahujeZavorku == True):
                zavorkaJeUvnitrUvozovek = self.detekujZdaZavorkaNeniUvnitrUvozovek(radek)
                if(zavorkaJeUvnitrUvozovek == False):
                    poleIndexuRadku.append(i)

        return(poleIndexuRadku)


    def detekujZdaZavorkaNeniUvnitrUvozovek(self, radek):

        zavorkaJeUvnitrUvozovek = False
        indexZavorky = radek.index('(')

        x = slice(0, indexZavorky)
        strPredZavorkou = radek[x]
        pocetApostrofuPredZavorkou = strPredZavorkou.count('\'')
        pocetPredZavokouJeSude = self.detekujZdaSeJednaOSudeCislo(pocetApostrofuPredZavorkou)

        x = slice(indexZavorky, len(radek)-1)
        strZaZavorkou = radek[x]
        pocetApostrofuZaZavorkou = strZaZavorkou.count('\'')
        pocetZaZavokouJeSude = self.detekujZdaSeJednaOSudeCislo(pocetApostrofuZaZavorkou)

        if(pocetPredZavokouJeSude == False):
            if(pocetZaZavokouJeSude == False):
                # pokud je oboje liche, pak to znamena, ze zavorka je uvnitr uvozovek
                zavorkaJeUvnitrUvozovek = True

        return(zavorkaJeUvnitrUvozovek)


    def detekujZdaSeJednaOSudeCislo(self, cislo):

        zbytek = cislo % 2

        if(zbytek == 0):
            jeToSudeCislo = True
        else:
            jeToSudeCislo = False

        return(jeToSudeCislo)


    def detekujSubstr(self, radek, subStr):

        try:
            ind = radek.index(subStr)
            radekObsahujeSubstr = True
        except:
            radekObsahujeSubstr = False

        return(radekObsahujeSubstr)


    def detekujPrvniPlatnyIfcClass(self, poleHashId):

        prvniIndex = 0

        for i in range(0, len(poleHashId)):
            hash = poleHashId[i]

            if (hash != ''):
                prvniIndex = i
                break

        return (prvniIndex)


    def unique(self, list1):

        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)

        return (unique_list)


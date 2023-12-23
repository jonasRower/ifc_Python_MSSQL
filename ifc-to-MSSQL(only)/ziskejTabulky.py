import vyhledejDataDavky
import copy

class vytvorTabulky:

    def __init__(self, poleRozdelenychRadku):

        poleHashId = self.vratPole1DDleIndexu(poleRozdelenychRadku, 0)
        poleClass = self.vratPole1DDleIndexu(poleRozdelenychRadku, 1)

        ifcClassesRadky = self.vratIfcClassParr(poleClass)
        ifcClasses = self.vratPole1DDleIndexu(ifcClassesRadky, 0)
        parametersArr = self.vratPole1DDleIndexu(ifcClassesRadky, 1)

        ifcClassesUniq = self.unique(ifcClasses)

        # vyhledva data po davce, tak aby mohl data zapisovat do DB
        self.vyhledavejDataPoDavce(ifcClasses, ifcClassesUniq, poleHashId, parametersArr)


    def getNazevTabulkyARadkyAll(self):
        return(self.nazevTabulkyARadkyAll)


    def vyhledavejDataPoDavce(self, ifcClasses, ifcClassesUniq, poleHashId, parametersArr):

        for i in range(0, len(ifcClassesUniq)):

            if(i == 22):
                a = 5

            ifcClass = ifcClassesUniq[i]
            vyhledejDataDavky.dataDavky(ifcClasses, ifcClass, poleHashId, parametersArr)


    def seskupPoleRozdelenychRadkuDleTabulek(self, poleHashId, parametersArr, nazvyTabulek, poleIndexuAll):

        nazevTabulkyARadkyAll = []

        for i in range(0, len(nazvyTabulek)):

            nazevTabulky = nazvyTabulek[i]
            indexyRadku = poleIndexuAll[i]

            rozdeleneRadkyTab = self.vratVsechnyRozdeleneRadkyDleTabulky(poleHashId, parametersArr, indexyRadku)

            nazevTabulkyARadky = []
            nazevTabulkyARadky.append(nazevTabulky)
            nazevTabulkyARadky.append(rozdeleneRadkyTab)

            nazevTabulkyARadkyAll.append(nazevTabulkyARadky)

        return(nazevTabulkyARadkyAll)


    def vratVsechnyRozdeleneRadkyDleTabulky(self, poleHashId, parametersArr, indexyRadku):

        rozdeleneRadkyTab = []

        for i in range(0, len(indexyRadku)):

            indexRadku = indexyRadku[i]
            hashId = poleHashId[indexRadku]
            parameters = parametersArr[indexRadku]

            radek = []
            radek.append(hashId)
            radek.append(parameters)

            rozdeleneRadkyTab.append(radek)

        return(rozdeleneRadkyTab)




    def vratIndexyVsechnyIndexyRadkuProIfcClasses(self, ifcClassesRadky, ifcClassesUniq):

        poleIndexuAll = []
        ifcClassesRadky = copy.deepcopy(ifcClassesRadky)

        for i in range(0, len(ifcClassesUniq)):

            ifcClass = ifcClassesUniq[i]

            if(ifcClass != ''):
                poleIndexu = self.ziskejPoleVsechIndexu(ifcClassesRadky, ifcClass)
            else:
                poleIndexu = []

            poleIndexuAll.append(poleIndexu)

        return(poleIndexuAll)



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




    def vratIfcClassParr(self, poleClass):

        ifcClassesArr = []

        for i in range(0, len(poleClass)):

            radek = poleClass[i]
            radekObsahujeZavoku = self.detekujSubstr(radek, '(')

            if(radekObsahujeZavoku == True):
                radekSpl = radek.split('(')
                ifcClass = radekSpl[0]

                obsahZavorky = radekSpl[1]
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

        cistyObsahZavorky = radek.replace(')', '')
        cistyObsahZavorky = cistyObsahZavorky.replace('\n', '')

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

    def unique(self, list1):

        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)

        return(unique_list)


class readIfc:

    def __init__(self):

        poleRadkuIfc = self.vratPoleradkuIfc()
        poleRozdelenychRadku = self.ziskejPoleRozdelenychRadku(poleRadkuIfc)

        self.poleHash = self.vratPole1DDleIndexu(poleRozdelenychRadku, 0)
        self.ifcClass = self.vratIfcClassParr(poleRozdelenychRadku)


    def getPoleHash(self):
        return(self.poleHash)


    def getIfcClass(self):
        return(self.ifcClass)


    def vratIfcClassParr(self, poleRozdelenychRadku):

        poleClass = self.vratPole1DDleIndexu(poleRozdelenychRadku, 1)

        ifcClassesArr = []

        for i in range(0, len(poleClass)):

            radek = poleClass[i]
            radekObsahujeZavoku = self.detekujSubstr(radek, '(')

            if(radekObsahujeZavoku == True):
                radekSpl = radek.split('(')
                ifcClass = radekSpl[0]

            else:
                ifcClass = ''

            ifcClassesArr.append(ifcClass)

        return(ifcClassesArr)


    def vratObsahZavorky(self, radek):

        indexZacZav = radek.index('(') + 1
        indexKonZav = radek.index(')')

        obsahZavorky = radek[indexZacZav:indexKonZav:1]
        seznamHashId = self.vratSeznamHashIdZavorky(obsahZavorky)

        return(seznamHashId)


    def vratSeznamHashIdZavorky(self, obsahZavorky):

        seznamHashId = []
        obsahZavorkySpl = obsahZavorky.split(',')

        for i in range(0, len(obsahZavorkySpl)):
            znakZavorky = obsahZavorkySpl[i]
            jeToHash = self.detekujSubstr(znakZavorky, '#')

            if(jeToHash == True):
                znakZavorky = znakZavorky.replace('(', '')
                seznamHashId.append(znakZavorky)

        return(seznamHashId)



    def ziskejPoleRozdelenychRadku(self, poleRadkuIfc):

        poleRozdelenychRadku = []

        for i in range(0, len(poleRadkuIfc)):

            radek = poleRadkuIfc[i]
            radekObsahujeOddelovac = self.detekujSubstr(radek, '=')

            if(radekObsahujeOddelovac == True):
                radekSpl = radek.split('=')
                split1 = radekSpl[0]
                split2 = radekSpl[1]

            else:
                split1 = ''
                split2 = radek

            split2 = self.odmazStrednikNaKonciRadku(split2)

            rozdelRadek = []
            rozdelRadek.append(split1)
            rozdelRadek.append(split2)

            poleRozdelenychRadku.append(rozdelRadek)

        return(poleRozdelenychRadku)


    def odmazStrednikNaKonciRadku(self, radek):

        radekBezZalomeni = radek.replace('\n', '')

        if(radekBezZalomeni != ''):
            posledniZnak = radekBezZalomeni[-1]
            if(posledniZnak == ';'):
                radekNew = radek[0:len(radekBezZalomeni)-1:1]
            else:
                radekNew = radekBezZalomeni
        else:
            radekNew = radekBezZalomeni


        return(radekNew)


    def detekujSubstr(self, radek, subStr):

        try:
            ind = radek.index(subStr)
            radekObsahujeSubStr = True
        except:
            radekObsahujeSubStr = False

        return(radekObsahujeSubStr)


    def vratPoleradkuIfc(self):

        adresa = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\2023\\Python\\IFC\\input\\AC20-FZK-Haus.ifc'

        with open(adresa, mode="r", encoding="utf-8") as f:

            linesOfFile = f.readlines()


        return(linesOfFile)


    def vratPole1DDleIndexu(self, pole2D, index):

        pole1D = []

        for i in range(0, len(pole2D)):

            radekPole = pole2D[i]
            try:
                hodnota = radekPole[index]
            except:
                hodnota = ''

            pole1D.append(hodnota)

        return (pole1D)



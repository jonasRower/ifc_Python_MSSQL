import pyodbc as odbccon
import prochazejTabulkami

class ifcJsTree:

    def __init__(self, id):

        self.ifcRadek = []
        self.potomci = []
        self.rodice = []

        self.vratIfcRadekAPotomky(id)
        self.radkyJson = self.vratPoleParents(self.potomci, self.rodice, self.ifcRadek)


    def getRadkyJson(self):
        return(self.radkyJson)


    def vratPoleParents(self, potomci, rodice, ifcRadky):

        radkyJson = []

        for i in range(0, len(rodice)):
            id = rodice[i]
            parent = self.vyhledejIndexRadkuKdeSeNachaziPotomek(potomci, id, rodice)
            text = ifcRadky[i]


            radekJson = self.vytvorRadekJson(id, parent, text)
            radkyJson.append(radekJson)

        return(radkyJson)


    def vytvorRadekJson(self, id, parent, text):

        if(text == None):
            text = 'missing data in database'

        radek = '                { "id": "' + str(id) + '", "parent": "' + str(parent) + '", "text": "' + text + '" },'

        return(radek)


    def vyhledejIndexRadkuKdeSeNachaziPotomek(self, potomci, potomek, rodice):

        parent = '#'

        for i in range(0, len(potomci)):
            potomciRodice = potomci[i]
            indexJeVPoli = self.detekujZdaSeIndexNachaziVPoli(potomek, potomciRodice)

            if(indexJeVPoli == True):
                parent = rodice[i]
                break

        return(parent)


    def detekujZdaSeIndexNachaziVPoli(self, index, pole):

        try:
            ind = pole.index(index)
            indexJeVPoli = True
        except:
            indexJeVPoli = False

        return(indexJeVPoli)


    def vratIfcRadekAPotomky(self, rodic):

        potomciAllStatus = []

        conn = self.pripojSeKDB()
        dataZDotazu = prochazejTabulkami.vratIfcRadek(conn, rodic)

        ifcRadek = dataZDotazu.getIfcRadek()
        potomci = dataZDotazu.getIfcPotomci()

        self.ifcRadek.append(ifcRadek)
        self.potomci.append(potomci)
        self.rodice.append(rodic)

        potomciAllStatus = self.vratPotomciStatus(potomci, rodic, potomciAllStatus)

        for i in range(0, len(potomciAllStatus)):
            status = potomciAllStatus[i][1]
            if(status == False):
                rodic = potomciAllStatus[i][0]
                potomciAllStatus[i][1] = True

                dataZDotazu = prochazejTabulkami.vratIfcRadek(conn, rodic)

                ifcRadek = dataZDotazu.getIfcRadek()
                potomci = dataZDotazu.getIfcPotomci()

                self.ifcRadek.append(ifcRadek)
                self.potomci.append(potomci)
                self.rodice.append(rodic)

                potomciAllStatus = self.vratPotomciStatus(potomci, rodic, potomciAllStatus)


        # zapisuje do self. ... tudiz nevraci nic

        #zastav na breakpointu a = 5 a pak dej breakpoint sem.
        #potomci nejsou 12, 934, 85
        #ale 12, 93_4 = 66, 85

    def vratPotomciStatus(self, potomci, rodic, potomciAllStatus):

        potomciStatusRodicNeww = []

        for i in range(0, len(potomci)):
            potomekInt = potomci[i]

            status = False
            potomciStatusRodic = []
            potomciStatusRodic.append(potomekInt)
            potomciStatusRodic.append(status)
            potomciStatusRodic.append(rodic)

            potomciStatusRodicNeww.append(potomciStatusRodic)

        potomciAllStatus = potomciAllStatus + potomciStatusRodicNeww

        return(potomciAllStatus)



    def pripojSeKDB(self):

        conn = odbccon.connect("DRIVER={SQL Server Native Client 11.0};"
                               "Server=DESKTOP-U6S885I\SQLEXPRESS;"
                               "Database=HumanResources;"
                               "Trusted_Connection=yes;")

        return (conn)



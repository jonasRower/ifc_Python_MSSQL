# opravuje dotazy, pokud dotazy neprobehnou databazi

# muze se stat, ze neodpovida pocet sloupcu, pak v tomto pripade,
# resp, pocet hodnot je nizsi nez pocet sloupcu
# pak v tom pripade doplnuje prazdne hodnoty
class opravChybu:

    def __init__(self, errorId, errMessage, dotaz):

        #dotaz = 'INSERT INTO  IFCPROPERTYSINGLEVALUE (hash_Id, col_1, col_2, col_3, col_4, col_5, col_6) VALUES (\'#27192\', \'Hole Has Wall\'s Side Material\', \'$\', \'IFCBOOLEAN\')'
        #errMessage = '[42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]Incorrect syntax near \'s\'. (102) (SQLExecDirectW); [42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]Unclosed quotation mark after the character string \')\'. (105)'

        pouzeZavorky = self.rozdelDotazNaPredAPoValues(dotaz)

        # pokud nenalezne id chyby, pak vraci puvodni data
        zavorkaNew = pouzeZavorky[1]


        if(errorId == '42000'):

            popisChyby = detekujPopisChyby(errMessage)
            chybneAOpraveneZnaky = popisChyby.getChybneAOpraveneZnaky()

            opraveneClenyZavorky = self.opravJednotliveClenyZavorky(pouzeZavorky[1], chybneAOpraveneZnaky)
            zavorkaNew = self.vytvorZavorku(opraveneClenyZavorky)


        if (errorId == '21S01'):

            pocetClenuZavorek = self.vratPocetClenuZavorek(pouzeZavorky)

            zavorkaNew = self.rozsirZavorkuOPrazdneCleny(pocetClenuZavorek, pouzeZavorky[1])
            self.dotazNew = self.opravDotazOSpravnouZavorku(dotaz, pouzeZavorky[1], zavorkaNew)


        self.dotazNew = self.opravDotazOSpravnouZavorku(dotaz, pouzeZavorky[1], zavorkaNew)



    def getDotazNew(self):
        return(self.dotazNew)


    def vytvorZavorku(self, opraveneClenyZavorky):

        zavorka = '('

        for i in range(0, len(opraveneClenyZavorky)):
            clenZavorky = opraveneClenyZavorky[i]
            zavorka = zavorka + clenZavorky

            if(i < len(opraveneClenyZavorky)-1):
                zavorka = zavorka + ', '
            else:
                zavorka = zavorka + ')'

        return(zavorka)


    def opravJednotliveClenyZavorky(self, zavorka, chybneAOpraveneZnaky):

        zavorkaCleny = self.vratPouzeTeloClenuZavorky(zavorka)
        opraveneClenyZavorky = []

        for i in range(0, len(zavorkaCleny)):
            clenZavorky = zavorkaCleny[i]
            clenZavorkyNew = self.opravClenZavorky(clenZavorky, chybneAOpraveneZnaky)

            clenZavorkyNew = '\'' + clenZavorkyNew + '\''

            opraveneClenyZavorky.append(clenZavorkyNew)

        return(opraveneClenyZavorky)


    def opravClenZavorky(self, clenZavorky, chybneAOpraveneZnaky):

        clenZavorkyNew = clenZavorky

        for i in range(0, len(chybneAOpraveneZnaky)):
            nahradCo = chybneAOpraveneZnaky[i][0]
            nahradCim = chybneAOpraveneZnaky[i][1]

            clenZavorkyNew = clenZavorkyNew.replace(nahradCo, nahradCim)

        return(clenZavorkyNew)


    def vratPouzeTeloClenuZavorky(self, zavorka):

        zavorkaCleny = zavorka.split(',')
        teloClenuZavorky = []

        for i in range(0, len(zavorkaCleny)):
            clenFull = zavorkaCleny[i]
            clenCisty = self.vratclenCisty(clenFull)

            teloClenuZavorky.append(clenCisty)

        return(teloClenuZavorky)


    def vratclenCisty(self, clenFull):

        indUvoz1 = clenFull.index('\'') + 1
        clenFullRevers = clenFull[::-1]

        indUvozEnd = clenFullRevers.index('\'')
        indUvoz2 = len(clenFull) - indUvozEnd - 1

        clenCisty = clenFull[indUvoz1:indUvoz2:1]

        return(clenCisty)


    def opravDotazOSpravnouZavorku(self, dotazPuvodni, zamenCo, zamenCim):

        dotazNew = dotazPuvodni.replace(zamenCo, zamenCim)

        return(dotazNew)


    def rozsirZavorkuOPrazdneCleny(self, pocetClenuZavorek, zavorka):

        prazdneCleny = self.vratPrazdneCleny(pocetClenuZavorek)

        if(prazdneCleny != ''):
            zavorkaNew = zavorka.replace(')', prazdneCleny)
        else:
            zavorkaNew = zavorka

        return(zavorkaNew)


    def vratPrazdneCleny(self, pocetClenuZavorek):

        rozdilVPoctuClenu = self.detekujOKollikRozsiritZavorku(pocetClenuZavorek)
        prazdneCleny = ''

        if(rozdilVPoctuClenu > 0):

            for i in range(0, rozdilVPoctuClenu):
                prazdneCleny = prazdneCleny + ', \'\''

            prazdneCleny = prazdneCleny + ')'

        return(prazdneCleny)


    def detekujOKollikRozsiritZavorku(self, pocetClenuZavorek):

        pocetClenu1 = pocetClenuZavorek[0]
        pocetClenu2 = pocetClenuZavorek[1]

        rozdil = pocetClenu1 - pocetClenu2

        return(rozdil)


    def vratPocetClenuZavorek(self, pouzeZavorky):

        pocetClenuZavorek = []

        for i in range(0, len(pouzeZavorky)):
            zavorka = pouzeZavorky[i]
            pocetClenuZavorky = self.vratPocetClenuZavorky(zavorka)

            pocetClenuZavorek.append(pocetClenuZavorky)

        return(pocetClenuZavorek)


    def rozdelDotazNaPredAPoValues(self, dotaz):

        pouzeZavorky = []
        dotazSplitValues = dotaz.split('VALUES')

        for i in range(0, len(dotazSplitValues)):
            zavorka = self.vratPouzeZavorku(dotazSplitValues[i])
            pouzeZavorky.append(zavorka)


        return(pouzeZavorky)


    def vratPocetClenuZavorky(self, zavorka):

        zavorakSpl = zavorka.split(',')
        pocetClenu = len(zavorakSpl)

        return(pocetClenu)


    def vratPouzeZavorku(self, radek):

        radekSpl = radek.split('(')
        zavorka = '(' + radekSpl[1]

        return(zavorka)


class detekujPopisChyby:

    def __init__(self, errMessage):

        seznamChyb = self.vratSeznamChyb(errMessage)
        seznamChybnychZnaku = self.vratSeznamChybnychZnaku(seznamChyb)
        self.chybneAOpraveneZnaky = self.vratKChybnymZnakumZnakySpravne(seznamChybnychZnaku)



    def getChybneAOpraveneZnaky(self):
        return(self.chybneAOpraveneZnaky)


    def vratKChybnymZnakumZnakySpravne(self, seznamChybnychZnaku):

        chybneAOpraveneZnaky = []

        for i in range(0, len(seznamChybnychZnaku)):
            chybnyZnak = seznamChybnychZnaku[i]
            opravenyZnak = chybnyZnak.replace('\'', '\'\'')

            chybnyAOpravenyZnak = []
            chybnyAOpravenyZnak.append(chybnyZnak)
            chybnyAOpravenyZnak.append(opravenyZnak)

            chybneAOpraveneZnaky.append(chybnyAOpravenyZnak)

        return(chybneAOpraveneZnaky)


    def vratSeznamChyb(self, errMessage):

        errMessageSpl = errMessage.split('[SQL Server]')
        seznamChyb = []

        for i in range(0, len(errMessageSpl)):
            radek = errMessageSpl[i]
            errSpl = radek.split('. (')

            if (len(errSpl) == 2):
                popisChyby = errSpl[0]
                seznamChyb.append(popisChyby)

        return (seznamChyb)

    def vratSeznamChybnychZnaku(self, seznamChyb):

        seznamChybnychZnaku = []

        for i in range(0, len(seznamChyb)):
            popisChyby = seznamChyb[i]
            chybnyZnak = self.vratChybnyZnakZPopisuChyby(popisChyby)
            chybnyZnak2 = chybnyZnak[0:len(chybnyZnak)-1:1]

            seznamChybnychZnaku.append(chybnyZnak2)

        return (seznamChybnychZnaku)

    def vratChybnyZnakZPopisuChyby(self, popisChyby):

        popisChybySpl = popisChyby.split(' ')
        chybnyZnak = popisChybySpl[len(popisChybySpl) - 1]

        return (chybnyZnak)



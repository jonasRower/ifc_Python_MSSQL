# vytvori tabulku, ktera spojuje jednotlive hash s nazvy tabulek

import vlozSQLdotazDoDB

class tabulkaOverview:

    def __init__(self, ifcClasses, poleHashId):

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


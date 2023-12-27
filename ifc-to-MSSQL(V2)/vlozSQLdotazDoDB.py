import sys
import pyodbc as odbccon
import SQLExceptions


class SQLDropTable:

    def __init__(self, nazevTabulky):

        dotazSQLDropTable = 'DROP TABLE IF EXISTS ' + nazevTabulky
        zapisDataDoDB(dotazSQLDropTable)


class SQLCreateTable:

    def __init__(self, nazevTabulky, nazvySloupcu):

        dotazSQLCreateTable = self.vytvorDotazCreateTable(nazevTabulky, nazvySloupcu)
        zapisDataDoDB(dotazSQLCreateTable)


    def vytvorDotazCreateTable(self, nazevTab, nazvySloupcu):

        sqlDotaz = 'CREATE TABLE ' + nazevTab + ' ('

        for i in range(0, len(nazvySloupcu)):
            nazevSloupce = nazvySloupcu[i][1]
            dataType = nazvySloupcu[i][0]

            sqlDotaz = sqlDotaz + '"' + nazevSloupce + '" ' + dataType

            if(i < len(nazvySloupcu)-1):
                sqlDotaz = sqlDotaz + ', '

        sqlDotaz = sqlDotaz + ')'

        return (sqlDotaz)



class SQLInsertInto:

    def __init__(self, nazevTabulky, typAnazvySloupcu, rozdeleneRadkyTab):

        sqlInsertIntoArr = self.vlozInsertIntoProVsechnyRadky(nazevTabulky, typAnazvySloupcu, rozdeleneRadkyTab)
        zapisDataDoDB(sqlInsertIntoArr)


    def vlozInsertIntoProVsechnyRadky(self, nazevTabulky, typAnazvySloupcu, rozdeleneRadkyTab):

        sqlInsertIntoArr = []
        nazvySloupcuZavorka = self.vratNazvySloupcuVZavorce(typAnazvySloupcu)

        for i in range(0, len(rozdeleneRadkyTab)):
            valuesJedenRadek = rozdeleneRadkyTab[i]
            valuesVZavorce = self.vytvorObsahZavorky(valuesJedenRadek, True)

            sqlInsertIntoJedenRadek = 'INSERT INTO ' + nazevTabulky + ' ' + nazvySloupcuZavorka + ' VALUES ' + valuesVZavorce
            sqlInsertIntoArr.append(sqlInsertIntoJedenRadek)

        return(sqlInsertIntoArr)


    def vratNazvySloupcuVZavorce(self, typAnazvySloupcu):

        nazvySloupcu = self.vratPole1DDleIndexu(typAnazvySloupcu, 1)
        nazvySloupcuZavorka = self.vytvorObsahZavorky(nazvySloupcu, False)

        return(nazvySloupcuZavorka)


    def vytvorObsahZavorky(self, dataZavorky, uvozovky):

        obsahZavorky = '('

        for i in range(0, len(dataZavorky)):
            hodnota = dataZavorky[i]

            if (uvozovky == True):
                hodnota = '\'' + str(hodnota) + '\''

            promennaJePrazdna = self.detekujZdaJePromennaPrazdna(hodnota)

            if (promennaJePrazdna == False):
                hodnota = hodnota.replace('\'\'', '\'')
            hodnota = hodnota.replace('\';\'', ';\'')


            obsahZavorky = obsahZavorky + hodnota

            if (i < len(dataZavorky) - 1):
                obsahZavorky = obsahZavorky + ', '
            else:
                obsahZavorky = obsahZavorky + ')'

        return (obsahZavorky)


    def detekujZdaJePromennaPrazdna(self, promena):

        promennaTrim = promena.replace('\'', '')
        promennaTrim = promennaTrim.strip()
        if(promennaTrim == ''):
            promennaJePrazdna = True
        else:
            promennaJePrazdna = False

        return(promennaJePrazdna)


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



class zapisDataDoDB:

    def __init__(self, SQLdotaz):

        conn = self.pripojSeKDB()
        cursor = conn.cursor()

        if type(SQLdotaz) == list:
            # pokud se jedna o seznam dotazu (pole)
            self.vykonejSeznamDotazu(SQLdotaz, cursor, conn)


        else:
            # pokud se jedna o dotaz jediny (string)
            self.vykonejDotaz(SQLdotaz, cursor, conn)



    def pripojSeKDB(self):

        conn = odbccon.connect("DRIVER={SQL Server Native Client 11.0};"
                               "Server=DESKTOP-U6S885I\SQLEXPRESS;"
                               "Database=humanResources;"
                               "Trusted_Connection=yes;")

        return(conn)


    def vykonejSeznamDotazu(self, seznamDotazu, cursor, conn):

        for i in range(0, len(seznamDotazu)):

            dotaz = seznamDotazu[i]
            self.vykonejDotaz(dotaz, cursor, conn)


    def vykonejDotaz(self, dotaz, cursor, conn):

        try:
            cursor.execute(dotaz)
            conn.commit()

        except:
            pass

        """
        except odbccon.Error as err:
            args = err.args
            errorId = args[0]
            message = args[1]

            self.opravDotaz(errorId, message, dotaz, cursor, conn)
        """


    def opravDotaz(self, errorId, message, dotaz, cursor, conn):

        # 10 pokusu na opravu chyby
        for i in range(0, 10):

            try:
                # opravi dotaz
                opravenyDotaz = SQLExceptions.opravChybu(errorId, message, dotaz)
                dotaz = opravenyDotaz.getDotazNew()

                # vlozi dotaz znovu
                cursor.execute(dotaz)
                conn.commit()

                # pokud vlozi data do DB, pak jiz dalsimi pokusy neprobiha
                break

            except:
                # probehne a vstoupi do dalsiho cyklu, cimz opravi dotaz znovu
                pass

import pyodbc as odbccon

class readMSSQL:

    def __init__(self):

        dotaz = 'SELECT * FROM  overview'

        conn = self.pripojSeKDB()
        dataZDotazu = self.vratDataZDotazu(dotaz, conn)

        print()


    def pripojSeKDB(self):

        conn = odbccon.connect("DRIVER={SQL Server Native Client 11.0};"
                               "Server=DESKTOP-U6S885I\SQLEXPRESS;"
                               "Database=HumanResources;"
                               "Trusted_Connection=yes;")

        return(conn)


    def vratDataZDotazu(self, dotaz, conn):

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM overview')

        dataPoRadcich = []

        for row in cursor:
            dataPoRadcich.append(row)

        tabulkaRozdelena = self.rozdelDataPoRadcichNaTabulku(dataPoRadcich)

        return(tabulkaRozdelena)


    def rozdelDataPoRadcichNaTabulku(self, dataZDotazu):

        tabulkaRozdelena = []

        for i in range(0, len(dataZDotazu)):
            radek = str(dataZDotazu[i])
            radekSpl = radek.split(', ')

            radekSplNew = self.odeberUvozovky(radekSpl)
            tabulkaRozdelena.append(radekSplNew)

        return(tabulkaRozdelena)


    def odeberUvozovky(self, radekSpl):

        radekSplNew = []

        for i in range(0, len(radekSpl)):
            bunka = radekSpl[i]
            bunkaNew = bunka.replace('\'','')
            bunkaNew = bunkaNew.replace('(', '')
            bunkaNew = bunkaNew.replace(')', '')
            bunkaNew = bunkaNew.strip()

            radekSplNew.append(bunkaNew)

        return(radekSplNew)
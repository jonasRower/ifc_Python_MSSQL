# slouzi k testovani

class printTxt:

    def __init__(self, data, cestaKSouboru):

        self.tiskniDataDoTxt(data, cestaKSouboru)


    def tiskniDataDoTxt(self, dataKTisku, adresa):
        dataWrite = ""

        f = open(adresa, 'w')

        for i in range(0, len(dataKTisku)):

            radek = dataKTisku[i]

            if (radek != False):
                radekStr = str(radek)
                dataWrite = dataWrite + radekStr + '\n'

        f.write(dataWrite)
        f.close()
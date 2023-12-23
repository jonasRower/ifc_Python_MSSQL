import nactiIfc
import ziskejTabulky
import vytvorSQLDotazy
import tiskniTxt


""""""
# vkladat data po davkach

ifc = nactiIfc.readIfc()
poleRozdelenychRadku = ifc.getPoleRozdelenychRadku()

dataTabulek = ziskejTabulky.vytvorTabulky(poleRozdelenychRadku)


nazevTabulkyARadkyAll = dataTabulek.getNazevTabulkyARadkyAll()

SQLDotazy = vytvorSQLDotazy.vytvorTabulky(nazevTabulkyARadkyAll)
dotazyCreateTable = SQLDotazy.getDotazyCreateTable()
dotazyInsertInto = SQLDotazy.getDotazyInsertInto()
dotazyDropTable = SQLDotazy.getDotazyDropTable()


# adresy pro vystup do txt - test
tiskAdresaCreateTable = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\2023\\Python\\IFC\\SQL\\sqlCreateTable.sql'
tiskAdresaInsertInto = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\2023\\Python\\IFC\\SQL\\sqlInsertInto.sql'
tiskAdresaDropTable = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\2023\\Python\\IFC\\SQL\\sqlDropTable.sql'

tiskniTxt.printTxt(dotazyCreateTable, tiskAdresaCreateTable)
tiskniTxt.printTxt(dotazyInsertInto, tiskAdresaInsertInto)
tiskniTxt.printTxt(dotazyDropTable, tiskAdresaDropTable)




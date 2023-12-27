import nactiIfc
import ziskejTabulky


# vklada data po davkach

ifc = nactiIfc.readIfc()
poleRozdelenychRadku = ifc.getPoleRozdelenychRadku()

dataTabulek = ziskejTabulky.vytvorTabulky(poleRozdelenychRadku)


print()






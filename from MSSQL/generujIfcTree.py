import os
import vykresliDataDoJsTree
import generujHtml
import nactiIfc


class ifcTree:

    def __init__(self, indOd, indDo):

        ifc = nactiIfc.readIfc()
        poleHash = ifc.getPoleHash()
        poleifcClass = ifc.getIfcClass()

        self.generujHtmlOdDo(indOd, indDo, poleHash, poleifcClass)


    def generujHtmlOdDo(self, indOd, indDo, poleHash, poleifcClass):

        for i in range(indOd, indDo):

            hashIfc = i
            hashExistuje = self.detekujZdaHashExistuje(hashIfc, poleHash)

            if(hashExistuje == True):
                ifcClass = poleifcClass[i].strip()
                dataJson = vykresliDataDoJsTree.ifcJsTree(hashIfc)
                radkyJson = dataJson.getRadkyJson()

                generujHtml.genHtml(radkyJson, hashIfc, ifcClass)


    def detekujZdaHashExistuje(self, index, poleHash):

        hashIndex = '#' + str(index)

        try:
            ind = poleHash.index(hashIndex)
            indexJeVIfc = True
        except:
            indexJeVIfc = False

        return(indexJeVIfc)



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


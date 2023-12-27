import vytvorOverview
import vyhledejDataDavky

class sendDataToDB:

    def __init__(self, ifcClasses, poleHashId, parametersArr):

        ifcClassesUniq = self.unique(ifcClasses)

        # vyhledva data po davce, tak aby mohl data zapisovat do DB
        hashIdProTabulkyAll = self.vyhledavejDataPoDavce(ifcClasses, ifcClassesUniq, poleHashId, parametersArr)

        # vytvori tabulku overview
        vytvorOverview.tabulkaOverview(ifcClassesUniq, hashIdProTabulkyAll)


    def vyhledavejDataPoDavce(self, ifcClasses, ifcClassesUniq, poleHashId, parametersArr):

        hashIdProTabulkyAll = []

        for i in range(0, len(ifcClassesUniq)):

            ifcClass = ifcClassesUniq[i]
            davka = vyhledejDataDavky.dataDavky(ifcClasses, ifcClass, poleHashId, parametersArr)

            hashIdProJednuTabulku = davka.getHashIdProJednuTabulku()
            hashIdProTabulkyAll.append(hashIdProJednuTabulku)

        return(hashIdProTabulkyAll)


    def unique(self, list1):

        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)

        return (unique_list)
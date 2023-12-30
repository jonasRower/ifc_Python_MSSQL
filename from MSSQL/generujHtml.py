
import os

class genHtml:

    def __init__(self, poleJson, hashIfc, ifcClass):

        radkyPred = self.definujRadkyPred()
        radkyZa = self.definujRadkyZa()

        htmlRadky = self.slozHtmlDohromady(radkyPred, poleJson, radkyZa)
        adresa = self.sestavAdresu(hashIfc, ifcClass)

        self.tiskniDataDoHtml(htmlRadky, adresa)


    def sestavAdresu(self, hashIfc, ifcClass):

        adresaPredClass = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\2023\\Python\\IFC\\ifcTree\\'
        adresaSlozky = adresaPredClass + ifcClass + '\\'

        adresaSlozkyExistuje = os.path.exists(adresaSlozky)

        if(adresaSlozkyExistuje == False):
            os.mkdir(adresaSlozky)

        nazevSouboru = 'ifcTree_' + str(hashIfc) + '.html'

        adresaPlna = adresaSlozky + nazevSouboru

        return(adresaPlna)


    def slozHtmlDohromady(self, radkyPred, poleJson, radkyZa):

        radkyHtml = []
        radkyHtml = radkyHtml + radkyPred
        radkyHtml = radkyHtml + poleJson
        radkyHtml = radkyHtml + radkyZa

        return(radkyHtml)


    def tiskniDataDoHtml(self, dataKTisku, adresaHtml):

        dataWrite = ""

        f = open(adresaHtml, 'w')

        for i in range(0, len(dataKTisku)):

            radek = dataKTisku[i]

            if(radek != False):
                radekStr = str(radek)
                dataWrite = dataWrite + radekStr + '\n'


        f.write(dataWrite)
        f.close()


    def definujRadkyPred(self):
        radkyPred = []
        radkyPred.append('<!DOCTYPE html>')
        radkyPred.append('<html lang="en" xmlns="http://www.w3.org/1999/xhtml">')
        radkyPred.append('<head>')
        radkyPred.append('    <meta charset="utf-8" />')
        radkyPred.append('    <title>Simple jsTree</title>')
        radkyPred.append(            '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css" />')
        radkyPred.append(            '    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.1/jquery.min.js"></script>')
        radkyPred.append(            '    <script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/jstree.min.js"></script>')
        radkyPred.append('')
        radkyPred.append('    <script type="text/javascript">')
        radkyPred.append('        $(function () {')
        radkyPred.append('')
        radkyPred.append('            var jsondata = [')

        return (radkyPred)

    def definujRadkyZa(self):
        radkyZa = []
        radkyZa.append('            ];')
        radkyZa.append('            createJSTree(jsondata);')
        radkyZa.append('        });')
        radkyZa.append('')
        radkyZa.append('        function createJSTree(jsondata) { ')
        radkyZa.append('            $(\'#SimpleJSTree\').jstree({')
        radkyZa.append('                \'core\': {')
        radkyZa.append('                    \'data\': jsondata')
        radkyZa.append('                }')
        radkyZa.append('            });')
        radkyZa.append('        }')
        radkyZa.append('    </script>')
        radkyZa.append('')
        radkyZa.append('</head>')
        radkyZa.append('<body>')
        radkyZa.append('   <div id="SimpleJSTree"></div>')
        radkyZa.append('</body>')
        radkyZa.append('</html>')

        return (radkyZa)
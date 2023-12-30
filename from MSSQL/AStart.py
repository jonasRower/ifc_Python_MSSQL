import nactiMSSQL
import prochazejTabulkami
import vykresliDataDoJsTree
import generujHtml
import generujIfcTree
import nactiIfc

#nactiMSSQL.readMSSQL()
#prochazejTabulkami.vyhledavejVTabulkach()

"""
dataJson = vykresliDataDoJsTree.ifcJsTree()
radkyJson = dataJson.getRadkyJson()

generujHtml.genHtml(radkyJson)
"""


generujIfcTree.ifcTree(0, 1000)
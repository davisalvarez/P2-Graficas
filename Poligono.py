from utilidades import *

class Poligono(object):

    def __init__(self):
        self.x = 0

    #earClipping algotitmo
    def triangulate(self, polygon, texturas, normales):

        triangulos = []
        triTexturas = []
        triNormales = []
        #Calculamos la orientación del poligon
        ori = self.polyOrientation(polygon)

        #verificamos si es CW
        if ori > 0:
            polygon.reverse()
            texturas.reverse()
            normales.reverse()
       #print(str(polygon))
        r = 0
        g = 0
        b = 0

        while(len(polygon) >= 3):
            pz = len(polygon)
            #print("len: "+str(len(polygon)))
            isTriRemove = True

            #print("poly: " + str(pz) + " vt: " + str(len(texcoords)))
            for point in range(pz):

                #Intentantamos armar un triangulo
                v1 = polygon[point]
                v2 = polygon[(point + 1) % pz]
                v3 = polygon[(point + 2) % pz]

                oriT = self.polyOrientation([v1, v2, v3])

                if oriT > 0:
                    continue

                #verificar si tiene punto adentro
                for x in polygon:
                    d1 = self.polyOrientation([x, v1, v2] )
                    d2 = self.polyOrientation([x, v2, v3])
                    d3 = self.polyOrientation([x, v3, v1])
                    if (d1 > 0 and d2 > 0 and d2 > 0):
                        #tiene punto
                        continue

                #obtenermos texturas
                vt1 = texturas[point]
                vt2 = texturas[(point + 1) % pz]
                vt3 = texturas[(point + 2) % pz]

                #obtenemos normales
                vn1 = normales[point]
                vn2 = normales[(point + 1) % pz]
                vn3 = normales[(point + 2) % pz]

                #print("_____"+str([vn1, vn2, vn3]))
                if vn1[0] == 0 and vn1[1] == 0 and vn1[2] == 0:
                    normal1 = crossProduct2x3(mySubtract(v3, v1),
                                             mySubtract(v2, v1))
                    vn1 = normalizarVector(normal1)
                if vn2[0] == 0 and vn2[1] == 0 and vn2[2] == 0:
                    normal2 = crossProduct2x3(mySubtract(v1, v2),
                                             mySubtract(v3, v2))
                    vn2 = normalizarVector(normal2)

                if vn3[0] == 0 and vn3[1] == 0 and vn3[2] == 0:
                    normal3 = crossProduct2x3(mySubtract(v2, v3),
                                             mySubtract(v1, v3))
                    vn3 = normalizarVector(normal3)


                triangulos.append([v1, v2, v3])
                triTexturas.append([vt1, vt2, vt3])
                triNormales.append([vn1, vn2, vn3])

                polygon.remove(polygon[(point + 1) % pz])
                texturas.remove(texturas[(point + 1) % pz])
                normales.remove(normales[(point + 1) % pz])
                isTriRemove = False
                break
            if isTriRemove:
                break
        return triangulos, triTexturas, triNormales

    def polyOrientation(self, polygon):
        sumPX = 0
        lar = len(polygon)

        for p in range(lar):
            sumPX += crossProduct2x2(polygon[p], polygon[(p + 1) % lar])
        return sumPX
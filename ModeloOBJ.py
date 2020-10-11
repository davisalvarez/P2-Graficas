import struct
from utilidades import *
from numpy import arccos, arctan2

class ModeloOBJ(object):

    def __init__(self, filename):
        m = open(filename,'r')

        self.lineas = m.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.traducir()


    def traducir(self):

        for line in self.lineas:
            if line:
                try:
                    tipo, valor = line.split(' ', 1)
                except:
                    continue

                #Vertices
                if tipo == 'v':
                    self.vertices.append(list(map(float,valor.split(' '))))
                # Normales
                elif tipo == 'vn':
                    self.normals.append(list(map(float,valor.split(' '))))
                # Texturas
                elif tipo == 'vt':
                    self.texcoords.append(list(map(float,valor.split(' '))))
                # Caras
                elif tipo == 'f':
                    caras =  valor.split(' ')
                    lista=[]
                    for cara in caras:
                        if cara!='':
                            c = cara.split('/')
                            vector=[]
                            for x in c:
                                try:
                                    vector.append(int(x))
                                except:
                                    continue
                            lista.append(vector)
                    self.faces.append(lista)
        print("Modelo cargado!")


class Texture(object):
    def __init__(self, filename):
        self.filename = filename
        self.traducir()

    def traducir(self):
        image = open(self.filename, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(color(r, g, b))

        image.close()
        print("Textura cargada!")

    def getColor(self, tx, ty):
        if tx >= 0 and tx <= 1 and ty >= 0 and ty <= 1:
            x = int(tx * self.width - 1)
            y = int(ty * self.height - 1)

            return self.pixels[y][x]
        else:
            return color(0, 0, 0)


    def getColorCood(self, tx, ty):
        if tx >= 0 and tx <= 1 and ty >= 0 and ty <= 1:
            x = int(tx * self.width - 1)
            y = int(ty * self.height - 1)

            return x, y
        else:
            return -1, -1

    def getColorByXY(self, tx, ty):
        if tx >= 0 and tx <= self.width - 1 and ty >= 0 and ty <= self.height - 1:
            return self.pixels[ty][tx]
        else:
            return color(0, 0, 0)

class Envmap(object):
    def __init__(self, filename):
        self.filename = filename
        self.traducir()

    def traducir(self):
        image = open(self.filename, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(color(r, g, b))

        image.close()
        print("Textura cargada!")

    def getColor(self, direction):
        direction = normalizarVector(direction)
        x = int((arctan2(direction[2], direction[0]) / (2 * 3.1416) + 0.5) * self.width)
        y = int(arccos(-direction[1]) / 3.1416 * self.height)

        return self.pixels[y][x]
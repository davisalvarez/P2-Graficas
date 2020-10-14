from utilidades import *
from ModeloOBJ import *
from Poligono import *
from Esfera import *
from numpy import cos, sin, tan
import numpy as np

BLACK = color(0,0,0)
WHITE = color(1,1,1)
YELLOW = color(1,1,0)

MAX_RECURSION_DEPTH = 3


def refractVector(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    # Snell's Law
    cosi = max(-1, min(1, np.dot(I, N)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        N = np.array(N) * -1

    eta = etai / etat
    k = 1 - eta * eta * (1 - (cosi * cosi))

    if k < 0:  # Total Internal Reflection
        return None

    R = eta * np.array(I) + (eta * cosi - k ** 0.5) * N
    return R / np.linalg.norm(R)


def fresnel(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    cosi = max(-1, min(1, np.dot(I, N)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    if sint >= 1:  # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
    return (Rs * Rs + Rp * Rp) / 2

class render(object):

    def __init__(self, width, height):
        self.width = 0
        self.height = 0
        self.default_color = BLACK
        self.vetex_color = WHITE
        self.pixels = []
        self.zBuffer = []
        self.xVP=0
        self.yVP = 0
        self.widthVP = 0
        self.heightVP = 0

        self.fov = 60
        self.scene = []
        self.camPosition = (0,5,5)
        self.pointLights = []
        self.ambientLight = None
        self.dirLight = None

        self.envmap = None

        self.glCreateWindow(width, height)

    def glInit(self):
        self.iniciarFramebuffer(BLACK)

    def glCreateWindow(self, w, h):
        self.width = w
        self.height = h
        self.iniciarFramebuffer(BLACK)
        self.glViewport(0, 0, w, h)

    def iniciarFramebuffer(self, _color):
        self.pixels = []
        for y in range(self.height):
            linea=[]
            for x in range(self.width):
                linea.append(_color)
            self.pixels.append(linea)


    # Z-Buffer A.K.A  buffer de profundidad
    def iniciarZbuffer(self):
        self.zBuffer = []
        for y in range(self.height):
            linea = []
            for x in range(self.width):
                linea.append(float('inf'))
            self.zBuffer.append(linea)

    def glViewport(self, x, y, width, height):
        self.xVP= x
        self.yVP = y
        self.widthVP = width
        self.heightVP = height

    def glClear(self):
        self.iniciarFramebuffer(self.default_color)
        self.iniciarZbuffer()


    def glClearColor(self, r, g, b):
        self.default_color=color(r, g, b)

    def glVertex(self, x, y):
        #pos X
        xIMG = self.xVP + (x+1)* (self.widthVP/2)
        #pos Y
        yIMG = self.yVP + (y+1)*(self.heightVP / 2)

        self.pintarPixelIMG(round(xIMG),round(yIMG))


    def pintarPixelIMG(self, x, y, _color = None):

        if x < self.xVP or x >= self.xVP + self.widthVP or y < self.yVP or y >= self.yVP + self.heightVP:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return
        try:
            self.pixels[y][x] = _color or color(self.vetex_color)
        except:
            pass

    def glColor(self, r, g, b):
        self.vetex_color=color(r, g, b)

    def glFinish(self):
        self.generar("gotham.bmp")
        #self.glZBuffer("profundidad.bmp")

    def glZBuffer(self, filename):

        imagen = open(filename, 'wb')

        #BITMAPFILEHEADER
        #14 Bytes

        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14+40+ self.width * self.height * 3))  #4
        imagen.write(word(0)) #2
        imagen.write(word(0)) #2
        imagen.write(dword(14+40)) #4

        #BITMAPINFOHEADER
        #40 Bytes

        imagen.write(dword(40)) #4
        imagen.write(dword(self.width)) #4
        imagen.write(dword(self.height)) #4
        imagen.write(word(1)) #2
        imagen.write(word(24)) # 2
        imagen.write(dword(0)) # 4
        imagen.write(dword(self.width * self.height * 3))  # 4

        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zBuffer[x][y] != float('inf'):
                    if self.zBuffer[x][y] < minZ:
                        minZ = self.zBuffer[x][y]

                    if self.zBuffer[x][y] > maxZ:
                        maxZ = self.zBuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zBuffer[x][y]
                if depth == float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                imagen.write(color(depth,depth,depth))

        imagen.close()

    def generar(self, filename):

        imagen = open(filename, 'wb')

        #BITMAPFILEHEADER
        #14 Bytes

        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14+40+ self.width * self.height * 3))  #4
        imagen.write(word(0)) #2
        imagen.write(word(0)) #2
        imagen.write(dword(14+40)) #4

        #BITMAPINFOHEADER
        #40 Bytes

        imagen.write(dword(40)) #4
        imagen.write(dword(self.width)) #4
        imagen.write(dword(self.height)) #4
        imagen.write(word(1)) #2
        imagen.write(word(24)) # 2
        imagen.write(dword(0)) # 4
        imagen.write(dword(self.width * self.height * 3))  # 4

        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4

        #self.pixels[11][11]=color(162,0,255)

        for y in range(self.height):
            for x in range(self.width):
                imagen.write(self.pixels[y][x])

        imagen.close()

    #Algoritmo de Ray Tracing
    def mcqueenRender(self):
        #Recorremos cada uno de los pixeles de la IMG
        for y in range(self.height):
            for x in range(self.width):

                # pasar valor de pixel a coordenadas NDC (-1 a 1)
                Px = 2 * ((x + 0.5) / self.width) - 1
                Py = 2 * ((y + 0.5) / self.height) - 1

                # FOV(angulo de vision), asumiendo que el near plane esta a 1 unidad de la camara
                t = tan(degree2radian(self.fov) / 2)
                r = t * self.width / self.height
                Px *= r
                Py *= t

                # Nuestra camara siempre esta viendo hacia -Z
                direction = [Px, Py, -1]
                direction = normalizarVector(direction)

                """
                material = None
                intersect = None

                # Revisamos cada rayo contra cada objeto
                for obj in self.scene:
                    hit = obj.ray_intersect(self.camPosition, direction)
                    if hit is not None:
                        if hit.distance < self.zBuffer[y][x]:
                            self.zBuffer[y][x] = hit.distance
                            material = obj.material
                            intersect = hit

                # Si hubo intersepcion, dibujamos el pixel
                if intersect is not None:
                    self.pintarPixelIMG(x, y, self.pointColor(material, intersect))
                """

                self.pintarPixelIMG(x, y, self.castRay(self.camPosition, direction))

    def scene_intercept(self, orig, direction, origObj = None):
        tempZbuffer = float('inf')
        material = None
        intersect = None

        # Revisamos cada rayo contra cada objeto
        for obj in self.scene:
            if obj is not origObj:
                hit = obj.ray_intersect(orig, direction)
                if hit is not None:
                    if hit.distance < tempZbuffer:
                        tempZbuffer = hit.distance
                        material = obj.material
                        intersect = hit
        """
        # Si hubo intersepcion, dibujamos el pixel
        if intersect is not None:
            self.pintarPixelIMG(x, y, self.pointColor(material, intersect))
        """
        return material, intersect

    def castRay(self, orig, direction, origObj = None, recursion = 0):

        material, intersect = self.scene_intercept(orig, direction, origObj)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.getColor(direction)
            return self.default_color

        objectColor = [material.diffuse[2] / 255,
                                material.diffuse[1] / 255,
                                material.diffuse[0] / 255]

        pLightColor = [0, 0, 0]

        ambientColor = [0, 0, 0]
        dirLightColor = [0,0,0]
        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        finalColor = [0,0,0]

        # Direccion de vista
        view_dir = mySubtract(self.camPosition, intersect.point)
        view_dir = normalizarVector(view_dir)

        if self.ambientLight:
            ambientColor = [self.ambientLight.strength * self.ambientLight.color[2] / 255,
                                     self.ambientLight.strength * self.ambientLight.color[1] / 255,
                                     self.ambientLight.strength * self.ambientLight.color[0] / 255]

        if self.dirLight:
            diffuseColor = np.array([0, 0, 0])
            specColor = np.array([0, 0, 0])
            shadow_intensity = 0

            #light_dir = np.array(self.dirLight.direction) * -1
            light_dir = myMultiplyExV(-1, self.dirLight.direction)

            # Calculamos el valor del diffuse color
            intensity = self.dirLight.intensity * max(0, dotProduct(light_dir, intersect.normal))
            diffuseColor = [intensity * self.dirLight.color[2] / 255,
                            intensity * self.dirLight.color[1] / 255,
                            intensity * self.dirLight.color[2] / 255]

            # Iluminacion especular
            reflect = self.reflectVector(intersect.normal, light_dir)  # Reflejar el vector de luz

            # spec_intensity: lightIntensity * ( view_dir dot reflect) ** especularidad
            spec_intensity = self.dirLight.intensity * (max(0, dotProduct(view_dir, reflect)) ** material.spec)
            specColor = [spec_intensity * self.dirLight.color[2] / 255,
                        spec_intensity * self.dirLight.color[1] / 255,
                        spec_intensity * self.dirLight.color[0] / 255]

            shadMat, shadInter = self.scene_intercept(intersect.point, light_dir, intersect.sceneObject)
            if shadInter is not None:
                shadow_intensity = 1

            #dirLightColor = (1 - shadow_intensity) * (diffuseColor + specColor)
            diffuseSpec = myAdd(diffuseColor, specColor)
            ambientShadow = myAdd(ambientColor, [1 - shadow_intensity,
                                                 1 - shadow_intensity,
                                                 1 - shadow_intensity])

            dirLightColor = myMultiply(diffuseSpec, ambientShadow)

        #if self.pointLight:
        for pointLight in self.pointLights:

            diffuseColor = [0, 0, 0]
            specColor = [0, 0, 0]
            shadow_intensity = 0

            # Sacamos la direccion de la luz para este punto
            light_dir = mySubtract(pointLight.position, intersect.point)
            light_dir = normalizarVector(light_dir)

            # Calculamos el valor del diffuse color dotProduct
            intensity = pointLight.intensity * max(0, dotProduct(light_dir, intersect.normal))
            diffuseColor = [intensity * pointLight.color[2] / 255,
                            intensity * pointLight.color[1] / 255,
                            intensity * pointLight.color[2] / 255]

            # Iluminacion especular
            view_dir = mySubtract(self.camPosition, intersect.point)
            view_dir = normalizarVector(view_dir)

            """
            funcion
            # R = 2 * (N dot L) * N - L
            reflect = 2 * dotProduct(intersect.normal, light_dir)
            reflect = myMultiplyExV(reflect, intersect.normal)
            reflect = mySubtract(reflect, light_dir)
            """
            reflect = self.reflectVector(intersect.normal, light_dir)

            # spec_intensity: lightIntensity * ( view_dir dot reflect) ** specularidad
            spec_intensity = pointLight.intensity * (max(0, dotProduct(view_dir, reflect)) ** material.spec)

            specColor = [spec_intensity * pointLight.color[2] / 255,
                        spec_intensity * pointLight.color[1] / 255,
                        spec_intensity * pointLight.color[0] / 255]

            shadMat, shadInter = self.scene_intercept(intersect.point, light_dir, intersect.sceneObject)
            if shadInter is not None:
                shadow_intensity = 1


            diffuseSpec = myAdd(diffuseColor, specColor)
            ambientShadow = myAdd(ambientColor, [1 - shadow_intensity,
                                                 1 - shadow_intensity,
                                                 1 - shadow_intensity])

            temp = myMultiply(diffuseSpec, ambientShadow)

            pLightColor = myAdd(pLightColor, temp)

        # Formula de iluminacion
        #finalColor = (ambientColor + (1 - shadow_intensity) * (diffuseColor + specColor)) * objectColor
        if material.matType == OPAQUE:

            finalColor = myAdd(ambientColor, pLightColor)
            finalColor = myAdd(finalColor, dirLightColor)

            if material.texture and intersect.texCoords:
                texColor = material.texture.getColor(intersect.texCoords[0], intersect.texCoords[1])

                finalColor = [finalColor[2] * texColor[2] / 255,
                                finalColor[1] * texColor[1] / 255,
                                finalColor[0] * texColor[0] / 255]

        elif material.matType == REFLECTIVE:
            #reflect = self.reflectVector(intersect.normal, np.array(direction) * -1)
            reflect = self.reflectVector(intersect.normal, view_dir)
            reflectColor = self.castRay(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflectColor = [reflectColor[2] / 255,
                            reflectColor[1] / 255,
                            reflectColor[0] / 255]


            finalColor = reflectColor + (1 - shadow_intensity) * specColor
            finalColor = [finalColor[0],
                            finalColor[1],
                            finalColor[2]]

            #print("- " + str(finalColor))
        """
        elif material.matType == TRANSPARENT:
            outside = np.dot(direction, intersect.normal) < 0
            #bias = 0.001 * intersect.normal

            bias = [reflectColor[2] * 0.001,
                    reflectColor[1] * 0.001,
                    reflectColor[0] * 0.001]

            kr = fresnel(intersect.normal, direction, material.ior)

            reflect = self.reflectVector(intersect.normal, np.array(direction) * -1)
            reflectOrig = np.add(intersect.point, bias) if outside else np.subtract(intersect.point, bias)
            reflectColor = self.castRay(reflectOrig, reflect, None, recursion + 1)
            reflectColor = np.array([reflectColor[2] / 255,
                                     reflectColor[1] / 255,
                                     reflectColor[0] / 255])

            if kr < 1:
                refract = refractVector(intersect.normal, direction, material.ior)
                refractOrig = np.subtract(intersect.point, bias) if outside else np.add(intersect.point, bias)
                refractColor = self.castRay(refractOrig, refract, None, recursion + 1)
                refractColor = np.array([refractColor[2] / 255,
                                         refractColor[1] / 255,
                                         refractColor[0] / 255])

            finalColor = reflectColor * kr + refractColor * (1 - kr) + (1 - shadow_intensity) * specColor
        """
        #Aplicamos el color de objeto
        finalColor = myMultiply(finalColor, objectColor)

        # Nos aseguramos que no suba el valor de color de 1

        r = min(1, finalColor[0])
        g = min(1, finalColor[1])
        b = min(1, finalColor[2])

        return color(r, g, b)

    def reflectVector(self, normal, dirVector):
        # R = 2 * (N dot L) * N - L
        reflect = 2 * dotProduct(normal, dirVector)
        reflect = myMultiplyExV(reflect, normal)
        reflect = mySubtract(reflect, dirVector)
        reflect = normalizarVector(reflect)
        return reflect
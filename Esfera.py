
from utilidades import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

WHITE = color(1,1,1)

class AmbientLight(object):
    def __init__(self, strength = 0, _color = WHITE):
        self.strength = strength
        self.color = _color

class PointLight(object):
    def __init__(self, position = (0,0,0), _color = WHITE, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0, ior = 1, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.matType = matType
        self.ior = ior

class Intersect(object):
    def __init__(self, distance, point, normal, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObject = sceneObject

class Esfera(object):
    def __init__(self, centro, radio, material):
        self.centro = centro
        self.radio = radio
        self.material = material

    def ray_intersect(self, orig, dir):

        L = mySubtract(self.centro, orig)
        tca = dotProduct(L, dir)
        l = magnitudVector(L)
        d = (l**2 - tca**2) ** 0.5
        if d > self.radio:
            return None

        thc = (self.radio ** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        dir=[dir[0]*t0,
             dir[1]*t0,
             dir[2]*t0]

        hit = myAdd(orig, dir)
        norm = mySubtract(hit, self.centro)
        norm = normalizarVector(norm)

        return Intersect(distance=t0,
                         point=hit,
                         normal=norm,
                         sceneObject=self)
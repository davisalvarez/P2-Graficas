"""
UVG
GRAFICAS POR COMPUTADORA - seccion 20

Davis Alvarez - 15842

"""
from render import *
from ModeloOBJ import *
from shader import *
from Esfera import *

ancho = 256
alto = 256

img = render(ancho, alto)

img.glInit()
img.glClearColor(0.5,1,0.36)
#img.glViewport(200,100,600,300)
img.glClear()

brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(diffuse = color(0.8,0.8,0.8), spec = 1024, matType = REFLECTIVE)

glass = Material( spec = 1024, ior = 1.5, matType = TRANSPARENT)

img.pointLight = PointLight(position = (-4,4,0), intensity = 1)
img.ambientLight = AmbientLight(strength = 0.1)

img.envmap = Envmap('envmap.bmp')

img.scene.append( Esfera(( 1, 1, -8), 1.5, brick) )
img.scene.append( Esfera(( 0, 0, -5), 0.5, glass) )
img.scene.append( Esfera((-3, 3, -10),  2, mirror) )
img.scene.append( Esfera((-3, -1.5, -10), 1.5, mirror) )

img.mcqueenRender()


"""
#______________________________

nieve = Material(diffuse=color(1, 1, 1), spec = 256)
wakanda = Material(diffuse=color(0, 0, 0))
botones = Material(diffuse=color(0.55, 0.26, 0.67), spec = 8)
zanahoria = Material(diffuse=color(1, 0.26, 0))
cielo = Material(diffuse=color(0.53,0.81,0.92), spec = 64)

img.pointLight = PointLight(position = (5,1,0), intensity = 1)
img.ambientLight = AmbientLight(strength = 0.3)

#Cuerpo
img.scene.append(Esfera((0, 10, -30), 4, nieve))
img.scene.append(Esfera((0, 2, -30), 5, nieve))
img.scene.append(Esfera((0, -8, -30), 7, nieve))

#Cara
img.scene.append(Esfera((1, 7.7, -25), 0.6, zanahoria))
img.scene.append(Esfera((-1.4, 9.6, -25), 0.7, cielo))
img.scene.append(Esfera((1.4, 9.6, -25), 0.7, cielo))

#boca
img.scene.append(Esfera((-1.8, 7.7, -27), 0.3, wakanda))
img.scene.append(Esfera((-1, 7.3, -27), 0.3, wakanda))
img.scene.append(Esfera((0, 6.8, -27), 0.3, wakanda)) #Centro
img.scene.append(Esfera((1.8, 7.7, -27), 0.3, wakanda))
img.scene.append(Esfera((1, 7.3, -27), 0.3, wakanda))

#Botones
img.scene.append(Esfera((0, 1.5, -25), 1, botones))
img.scene.append(Esfera((0, -1.8, -25), 1.2, botones))
img.scene.append(Esfera((0, -7, -25), 2.3, botones))
"""



img.glFinish() #5







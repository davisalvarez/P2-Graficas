"""
UVG
GRAFICAS POR COMPUTADORA - seccion 20

Davis Alvarez - 15842

"""
from render import *
from ModeloOBJ import *
from shader import *
from Esfera import *

ancho = 1024
alto = 512

img = render(ancho, alto)

img.glInit()
img.glClearColor(0.5,1,0.36)
#img.glViewport(200,100,600,300)
img.glClear()

espejoR = Material(diffuse = color(0.8,0,0), spec = 1024, matType = REFLECTIVE)
espejo = Material(diffuse = color(0.8,0.9,1), spec = 1024, matType = REFLECTIVE)
#glass = Material( spec = 1024, ior = 1.5, matType = TRANSPARENT)

#_________________________________________________________________________________
#Namek suns

img.pointLights.append(PointLight(position = (-4,-5,0), intensity = 0.4))
img.pointLights.append(PointLight(position = (2,3,0), intensity = 0.6))
img.dirLight = DirectionalLight(direction = (0, -2, -1), intensity = 0.2)
img.ambientLight = AmbientLight(strength = 0.2)

img.envmap = Envmap('textures/db3.bmp')

#_________________________________________________________________________________
#Dragon Balls

ballMat1 = Material(texture = Texture('textures/ball1.bmp'))
ballMat2 = Material(texture = Texture('textures/ball2.bmp'))
ballMat3 = Material(texture = Texture('textures/ball3.bmp'))
ballMat4 = Material(texture = Texture('textures/ball4.bmp'))
ballMat5 = Material(texture = Texture('textures/ball5.bmp'))
ballMat6 = Material(texture = Texture('textures/ball6.bmp'))
ballMat7 = Material(texture = Texture('textures/ball7.bmp'))

img.scene.append( Esfera(( -13, -4, -17), 1.5, ballMat1) )
img.scene.append( Esfera(( -8, -4, -17), 1.5, ballMat5) )
img.scene.append( Esfera(( -11, -1, -18), 1.5, ballMat7) )
img.scene.append( Esfera(( -15, -0.5, -18), 1.5, ballMat3) )
img.scene.append( Esfera(( -7, -0.5, -18), 1.5, ballMat2) )
img.scene.append( Esfera(( -11, 2.5, -18), 1.5, ballMat6) )

img.scene.append( Esfera(( 0, -4.5, -16), 1.5, ballMat4) )
#_________________________________________________________________________________
#Kakarot's Box

img.scene.append( AABBX((-10, -6, -20), (10, 0.5, 10) , espejo ) )
img.scene.append( AABBX((-15, -4.5, -20), (0.5, 3, 10) , espejoR ) )
img.scene.append( AABBX((-5, -4.5, -20), (0.5, 3, 10) , espejoR ) )
img.scene.append( AABBX((-10, -4.5, -25), (10, 3, 0.5) , espejoR ) )
img.scene.append( AABBX((-10, -5, -15), (10, 1.5, 0.5) , espejoR ) )

#_________________________________________________________________________________
#Arch

RedWoodMat = Material(texture = Texture('textures/redWood.bmp'))

img.scene.append( AABBX((10, 0, -50), (3, 40, 3) , RedWoodMat ) ) #Poste
img.scene.append( AABBX((40, 0, -50), (3, 40, 3) , RedWoodMat ) ) #Poste
img.scene.append( AABBX((25, 12, -50), (45, 3, 3) , RedWoodMat ) ) #Base Pequeña
img.scene.append( AABBX((25, 18, -50), (55, 3, 3) , RedWoodMat ) )   #Base Grande
img.scene.append( AABBX((25, 16, -50), (3, 5, 3) , RedWoodMat ) ) #Poste


img.scene.append( Esfera((25, 23.5, -50), 3.5, espejo) ) #bombilla Grande
img.scene.append( Esfera((4, 8.5, -50), 2, espejo) ) #bombilla pequeña
img.scene.append( Esfera((46, 8.5, -50), 2, espejo) ) #bombilla pequeña

#_________________________________________________________________________________

img.mcqueenRender()

img.glFinish() #5







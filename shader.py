from utilidades import *
import random as rn

#______________________________ Proyecto______________________________

def ruidoso(render, **kwargs):
    v1, v2, v3 = kwargs['verts']
    na, nb, nc = kwargs['normals']
    u, v, w = kwargs['baryCoords']

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = (nx, ny, nz)
    intensidad = dotProduct(normal, render.light)

    #print(str(intensidad))
    r = rn.random()
    g = rn.random()
    b = rn.random()

    if intensidad <0:
        intensidad = intensidad*-1

    b *= intensidad
    g *= intensidad
    r *= intensidad

    return r, g, b

def toonD(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = (nx,ny,nz)
    intensidad = dotProduct(normal, render.light)

    if intensidad < 0:
        intensidad = 0
    elif intensidad < 0.3:
        intensidad = 0.2
    elif intensidad < 0.6:
        intensidad = 0.4
    elif intensidad < 0.9:
        intensidad = 0.6
    else:
        intensidad = 1

    if render.active_texture:
        tx = ta[0] * u + tb[0] * v + tc[0] * w
        ty = ta[1] * u + tb[1] * v + tc[1] * w

        texColor = render.active_texture.getColor(tx, ty)

        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    b *= intensidad
    g *= intensidad
    r *= intensidad

    return r, g, b

def mapaNormales(render, **kwargs):
    n, t, bt = kwargs['espacioTan']
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    tx = ta[0] * u + tb[0] * v + tc[0] * w
    ty = ta[1] * u + tb[1] * v + tc[1] * w

    if render.active_texture:
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    if render.active_normalMap:
        texNormal = render.active_normalMap.getColor(tx, ty)
        texNormal = [(texNormal[2] /255)*2 -1 ,(texNormal[1] /255)*2 -1,(texNormal[0] /255)*2 -1]

        tanMatrix = [[t[0], bt[0],n[0]],
                     [t[1], bt[1],n[1]],
                     [t[2], bt[2],n[2]]]

        luz =  [[render.light[0]],
                [render.light[1]],
                [render.light[2]]]

        luz = multiplicarMatriz(tanMatrix, luz)

        luz = [luz[0][0],
                luz[1][0],
                luz[2][0]]

        #print(luz)

        luz = normalizarVector(luz)
        intensity = dotProduct(texNormal, luz)
    else:
        nx = na[0] * u + nb[0] * v + nc[0] * w
        ny = na[1] * u + nb[1] * v + nc[1] * w
        nz = na[2] * u + nb[2] * v + nc[2] * w

        normal = (nx, ny, nz)
        intensity = dotProduct(normal, render.light)

    if intensity > 1:
        intensity = 1

    b *= intensity
    g *= intensity
    r *= intensity
    print(intensity)
    print(str(r) + " " + str(g) + " " + str(b))



    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0

#______________________________ Proyecto______________________________


def gourad(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta[0] * u + tb[0] * v + tc[0] * w
        ty = ta[1] * u + tb[1] * v + tc[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = (nx, ny, nz)
    intensity =  dotProduct(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0



#ejemplo de la tierra
def sombreadoCool(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta[0] * u + tb[0] * v + tc[0] * w
        ty = ta[1] * u + tb[1] * v + tc[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = (nx, ny, nz)

    intensity = dotProduct(normal, render.light)
    if intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if render.active_texture2:
        texColor = render.active_texture2.getColor(tx, ty)

        b += (texColor[0] / 255) * (1 - intensity)
        g += (texColor[1] / 255) * (1 - intensity)
        r += (texColor[2] / 255) * (1 - intensity)
        #print("r "+str(r)+" g "+str(g)+" b "+str(b))

    return r, g, b

def unlit(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta[0] * u + tb[0] * v + tc[0] * w
        ty = ta[1] * u + tb[1] * v + tc[1] * w
        texColor = render.active_texture.getColor(tx,ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    return r, g, b

def flat(render, **kwargs):
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta[0] * u + tb[0] * v + tc[0] * w
        ty = ta[1] * u + tb[1] * v + tc[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    #print(str(A)+" - "+str(A)+" - "+str(A))
    normal = crossProduct2x3(mySubtract(B, A), mySubtract(C, A))
    normal = normalizarVector(normal)
    intensity = dotProduct(normal, render.light)
    #print(str(intensity))
    b *= intensity
    g *= intensity
    r *= intensity
    #print(str(r) + " " + str(g) + " " + str(b))
    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0
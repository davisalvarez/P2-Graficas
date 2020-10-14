
import struct

def color(r, g, b):
    #print(str(r)+" "+str(g)+" "+str(b))
    return bytes([round(b * 255), round(g * 255), round(r * 255)])

#Reserva 1 Byte en memoria
def char(c):
    return struct.pack('=c', c.enconde('ascii'))

#Reserva 2 Byte en memoria
def word(w):
    return struct.pack('=h',w)

#Reserva 4 Byte en memoria
def dword(d):
    return struct.pack('=l',d)

#Funciones matematicas:

#Producto cruz
def crossProduct2x2(pointA, pointB):
    return (pointA[0]*pointB[1]) - (pointA[1]*pointB[0])

#Producto cruz
def crossProduct2x3(pointA, pointB):
    res = []
    res.append(pointA[1] * pointB[2] - pointA[2] * pointB[1])
    res.append(pointA[2] * pointB[0] - pointA[0] * pointB[2])
    res.append(pointA[0] * pointB[1] - pointA[1] * pointB[0])
    return res

#Producto punto
def dotProduct(pointA, pointB):
    product = 0
    for i in range(len(pointA)):
        product = product + pointA[i] * pointB[i]

    return product

#multiplicar Matriz 4x4
def multiplicarMatriz(A, B):
    # matriz resultante
    #print(B)
    resMatrix = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]

    for i in range(len(A)): #Filas
        for j in range(len(B[0])):#Columnas
            for k in range(len(B)):
                resMatrix[i][j] += A[i][k] * B[k][j]

    return resMatrix

#resta de puntos
def mySubtract(list1, list2):
    resta = []
    if (len(list2) >= len(list1)):
        for i in range(len(list1)):
            resta.append(list1[i]-list2[i])
    return resta

#Suma de puntos
def myAdd(list1, list2):
    suma = []
    if (len(list2) >= len(list1)):
        for i in range(len(list1)):
            #print(str(list1[i])+" + "+str(list2[i]))
            suma.append(list1[i] + list2[i])
    return suma

#Multiplicacion de puntos
def myMultiply(list1, list2):
    mult = []
    #print(list1)
    if (len(list2) >= len(list1)):
        for i in range(len(list1)):
            mult.append(list1[i] * list2[i])
    return mult

#Multiplicacion de Escalar x Vector
def myMultiplyExV(escalar, vector):
    mult = []
    for i in range(len(vector)):
        mult.append(vector[i] * escalar)
    return mult

#Normalizar vector:
def normalizarVector(var):
    try:
        #largo del vector
        vector = [var[0],
                  var[1],
                  var[2]]

        largo =  (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5
        vector[0] = vector[0] / largo
        #print('vector '+str(largo))
        vector[1] = vector[1] / largo
        vector[2] = vector[2] / largo
    except ZeroDivisionError:
        print("Cero!!!!!!!!!!")
        return (0,0,0)
    return  vector

def magnitudVector(vector):
    try:
        #largo del vector
        largo =  (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5
    except ZeroDivisionError:
        #print("Cero!!!!!!!!!!")
        return 0
    return  largo

#Calcula coordenadas Barycentricas
def baryCoords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((B[1] - C[1])*(P[0] - C[0]) + (C[0] - B[0])*(P[1] - C[1]) ) /
              ((B[1] - C[1])*(A[0]- C[0]) + (C[0] - B[0])*(A[1] - C[1])) )

        v = ( ((C[1] - A[1])*(P[0] - C[0]) + (A[0] - C[0])*(P[1] - C[1]) ) /
              ((B[1] - C[1])*(A[0] - C[0]) + (C[0] - B[0])*(A[1] - C[1])) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

def degree2radian(beta):
    return beta * 3.1416/180

#Obtener Matriz inversa
def invertirMatriz(m):
    det = determinanteMatriz(m)

    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]
    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = complementarioMenor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * determinanteMatriz(minor))
        cofactors.append(cofactorRow)
    cofactors = matrizTranspuesta(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/det
    return cofactors

#obtener la transpuesta de una matriz
def matrizTranspuesta(m):
    return list(map(list,zip(*m)))

def complementarioMenor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

#Obtener el determinante de un matriz
def determinanteMatriz(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    det = 0
    for c in range(len(m)):
        det += ((-1)**c)*m[0][c]*determinanteMatriz(complementarioMenor(m,0,c))
    return det







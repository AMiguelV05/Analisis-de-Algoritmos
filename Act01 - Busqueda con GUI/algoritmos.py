import numpy as np

def generar_datos(n):
    listaDatos = np.random.randint(1, n+1, size=n)
    return listaDatos

def busqueda_lineal(lista, x):
    for elemento in lista:
        if elemento == x:
            return True
    return False

def busqueda_binaria(lista, x):
    lista.sort()
    izquierda = 0
    derecha = len(lista)-1
    while izquierda <= derecha:
        medio = (izquierda+derecha)//2
        if lista[medio] == x:
            return True
        elif lista[medio] > x:
            derecha = medio-1
        else: izquierda = medio+1
    return False
